import sys
import os
import re
import argparse
import tempfile
from pathlib import Path
from typing import Dict, Tuple
import requests
from urllib.parse import urlparse


class Colors:
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class DiscordToGoFile:
    
    GOFILE_API_BASE = "https://api.gofile.io"
    CHUNK_SIZE = 8192
    TIMEOUT = 30
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.original_filename = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def log(self, message: str, level: str = "info"):
        if not self.verbose:
            return
        
        icons = {"info": "→", "success": "✓", "error": "✗"}
        colors = {"info": Colors.CYAN, "success": Colors.GREEN, "error": Colors.RED}
        
        icon = icons.get(level, "·")
        color = colors.get(level, "")
        
        print(f"{color}{icon}{Colors.RESET} {message}")
    
    def separator(self, char: str = "─"):
        if self.verbose:
            print(char * 70)
    
    def validate_discord_url(self, url: str) -> bool:
        patterns = [
            r'https?://cdn\.discordapp\.com/',
            r'https?://media\.discordapp\.net/',
            r'https?://cdn\.discord\.com/'
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def extract_filename(self, url: str) -> str:
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]
        
        from urllib.parse import unquote
        filename = unquote(filename)
        
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        if '.' not in filename:
            filename = f"discord_file_{hash(url) % 10000}.bin"
        
        return filename
    
    def format_size(self, size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def download_from_discord(self, url: str) -> Tuple[str, int]:
        if not self.validate_discord_url(url):
            raise ValueError("URL Discord invalide")
        
        print(f"\n{Colors.BOLD}[1/3] Telechargement{Colors.RESET}")
        self.separator()
        
        try:
            head = self.session.head(url, timeout=self.TIMEOUT, allow_redirects=True)
            total_size = int(head.headers.get('content-length', 0))
            
            filename = self.extract_filename(url)
            self.log(f"Fichier: {filename}")
            
            if total_size > 0:
                self.log(f"Taille: {self.format_size(total_size)}")
            
            response = self.session.get(url, stream=True, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            self.original_filename = filename
            
            downloaded = 0
            print()
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if self.verbose and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            bar_len = 50
                            filled = int(bar_len * downloaded / total_size)
                            bar = '█' * filled + '░' * (bar_len - filled)
                            
                            mb_down = downloaded / (1024 * 1024)
                            mb_total = total_size / (1024 * 1024)
                            
                            print(f"\r  [{bar}] {percent:5.1f}% | {mb_down:6.2f}/{mb_total:.2f} MB", 
                                  end='', flush=True)
            
            if self.verbose and total_size > 0:
                print()
            
            file_size = os.path.getsize(temp_path)
            print()
            self.log("Telechargement terminé", "success")
            
            return temp_path, file_size
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise Exception("Accès refusé (token expiré)")
            elif e.response.status_code == 404:
                raise Exception("Fichier non trouvé")
            else:
                raise Exception(f"Erreur HTTP {e.response.status_code}")
        except requests.exceptions.Timeout:
            raise Exception("Timeout")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur réseau: {str(e)}")
    
    def get_gofile_server(self) -> str:
        print(f"\n{Colors.BOLD}[2/3] Sélection du serveur{Colors.RESET}")
        self.separator()
        
        try:
            response = self.session.get(f"{self.GOFILE_API_BASE}/servers", timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != 'ok':
                raise Exception("Impossible d'obtenir les serveurs")
            
            servers = data.get('data', {}).get('servers', [])
            if not servers:
                raise Exception("Aucun serveur disponible")
            
            server = servers[0]['name']
            self.log(f"Serveur: {server}")
            self.log("Prêt pour l'upload", "success")
            
            return server
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur serveur: {str(e)}")
    
    def upload_to_gofile(self, file_path: str, server: str, filename: str) -> Dict:
        file_size = os.path.getsize(file_path)
        
        print(f"\n{Colors.BOLD}[3/3] Upload vers GoFile{Colors.RESET}")
        self.separator()
        
        self.log(f"Envoi: {filename}")
        self.log(f"Taille: {self.format_size(file_size)}")
        
        upload_url = f"https://{server}.gofile.io/contents/uploadfile"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f)}
                response = self.session.post(upload_url, files=files, timeout=300)
                response.raise_for_status()
                data = response.json()
            
            if data.get('status') != 'ok':
                raise Exception(f"Erreur GoFile: {data.get('message', 'Inconnue')}")
            
            self.log("Upload terminé", "success")
            
            return data.get('data', {})
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                raise Exception("Serveur GoFile indisponible")
            else:
                raise Exception(f"Erreur HTTP {e.response.status_code}")
        except requests.exceptions.Timeout:
            raise Exception("Timeout")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur réseau: {str(e)}")
    
    def process(self, discord_url: str) -> Dict:
        temp_file = None
        
        try:
            temp_file, file_size = self.download_from_discord(discord_url)
            
            clean_filename = self.original_filename
            
            server = self.get_gofile_server()
            
            upload_data = self.upload_to_gofile(temp_file, server, clean_filename)
            
            return {
                'filename': clean_filename,
                'size': file_size,
                'size_formatted': self.format_size(file_size),
                'server': server,
                'download_page': upload_data.get('downloadPage', ''),
                'file_id': upload_data.get('fileId', ''),
                'parent_folder': upload_data.get('parentFolder', '')
            }
            
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def display_results(self, result: Dict):
        print(f"\n{Colors.BOLD}{Colors.GREEN}═══ TRANSFERT TERMINE ═══{Colors.RESET}")
        self.separator("═")
        
        print(f"\n{Colors.BOLD}Fichier{Colors.RESET}")
        print(f"  Nom      : {result['filename']}")
        print(f"  Taille   : {result['size_formatted']}")
        
        print(f"\n{Colors.BOLD}Serveur{Colors.RESET}")
        print(f"  GoFile   : {result['server']}")
        
        print(f"\n{Colors.BOLD}Lien{Colors.RESET}")
        print(f"  {Colors.GREEN}{result['download_page']}{Colors.RESET}")
        
        print()
        self.separator("═")


def main():
    parser = argparse.ArgumentParser(
        description="Transfert Discord vers GoFile",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('url', nargs='?', help="URL Discord CDN")
    parser.add_argument('-q', '--quiet', action='store_true', help="Mode silencieux")
    parser.add_argument('--no-pause', action='store_true', help="Pas de pause à la fin")
    
    args = parser.parse_args()
    
    discord_url = args.url
    
    if not discord_url:
        print("═" * 34)
        print(f"{Colors.BOLD}{Colors.CYAN}Discord to Gofile - MADE BY RAGEUI{Colors.RESET}")
        print("═" * 34)
        discord_url = input(f"\n{Colors.CYAN}URL Discord{Colors.RESET} → ").strip()
        
        if not discord_url:
            print(f"\n{Colors.RED}✗ Aucune URL fournie{Colors.RESET}\n")
            if not args.no_pause:
                input(f"{Colors.GRAY}Entrée pour quitter...{Colors.RESET}")
            sys.exit(1)
    
    uploader = DiscordToGoFile(verbose=not args.quiet)
    
    try:
        result = uploader.process(discord_url)
        uploader.display_results(result)
        
        if not args.no_pause:
            print(f"\n{Colors.GRAY}Entrée pour quitter...{Colors.RESET}")
            input()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}✗ Annulé{Colors.RESET}\n")
        if not args.no_pause:
            input(f"{Colors.GRAY}Entrée pour quitter...{Colors.RESET}")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n{Colors.BOLD}{Colors.RED}✗ ERREUR{Colors.RESET}")
        print(f"  {str(e)}\n")
        if not args.no_pause:
            input(f"{Colors.GRAY}Entrée pour quitter...{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()