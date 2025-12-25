# 🚀 Discord → GoFile

Petit utilitaire simple pour transférer rapidement un fichier depuis une URL CDN Discord vers GoFile.io, sans passer par un téléchargement local puis un ré-upload.

## Usage rapide
1. Téléchargez `discord_to_gofile.exe` (ou compilez depuis la source).
2. Lancez-le (double‑clic ou depuis un terminal).
3. Collez l'URL Discord CDN quand le programme le demande (ex. `https://cdn.discordapp.com/attachments/.../fichier.ext`).
4. Récupérez le lien GoFile affiché à la fin.

## Points importants
- Les liens Discord expirés ou protégés ne fonctionneront pas.
- GoFile peut imposer des limites de taille ou des restrictions ; les très gros fichiers peuvent échouer.
- Les fichiers temporaires sont supprimés après l'upload.

## Compiler depuis la source (rapide)
1. git clone https://github.com/RageUI-dev/Discord-to-Gofile-tool.git
2. Suivez les instructions de build du projet (dépend du langage utilisé).
3. Lancez le binaire généré.

## Dépannage
- "URL invalide" : vérifiez que l'URL contient `cdn.discordapp.com` et pointe directement vers le fichier.
- Upload échoué : réessayez plus tard (limite GoFile) ou testez un autre fichier.

---

Pour toute question, ouvrez une issue dans le dépôt ou me contacter via discord : **rageui**.
