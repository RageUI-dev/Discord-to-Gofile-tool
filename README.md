# Discord to GoFile

Un outil simple pour transférer des fichiers depuis Discord CDN vers GoFile.

## 📋 Prérequis

- Python 3.6+
- Module `requests`

## 🚀 Installation

```bash
git clone https://github.com/votre-username/discord-to-gofile.git
cd discord-to-gofile
pip install requests
```

## 💻 Utilisation

### Mode interactif

```bash
python discord_to_gofile.py
```

Le script vous demandera l'URL Discord.

### Mode ligne de commande

```bash
python discord_to_gofile.py "https://cdn.discordapp.com/attachments/..."
```

### Options

```bash
python discord_to_gofile.py [URL] [OPTIONS]

Options:
  -q, --quiet      Mode silencieux
  --no-pause       Pas de pause à la fin
  -h, --help       Affiche l'aide
```

## 📝 Exemples

```bash
# Transfert simple
python discord_to_gofile.py "https://cdn.discordapp.com/attachments/123/456/file.zip"

# Mode silencieux
python discord_to_gofile.py -q "https://cdn.discordapp.com/attachments/123/456/file.zip"

# Sans pause (utile pour scripts)
python discord_to_gofile.py --no-pause "https://cdn.discordapp.com/attachments/123/456/file.zip"
```

## ✨ Fonctionnalités

- ✅ Support des URLs Discord CDN (cdn.discordapp.com, media.discordapp.net, cdn.discord.com)
- ✅ Barre de progression pour le téléchargement
- ✅ Préservation du nom de fichier original
- ✅ Gestion des erreurs (timeout, 403, 404, etc.)
- ✅ Nettoyage automatique des fichiers temporaires
- ✅ Interface colorée et claire

## 🔧 Dépannage

### Erreur "Accès refusé (token expiré)"
Le lien Discord a expiré. Générez un nouveau lien.

### Erreur "Fichier non trouvé"
Vérifiez que l'URL est correcte et que le fichier existe toujours.

### Erreur "Timeout"
Votre connexion est trop lente ou instable. Réessayez.

## 📄 Licence

MIT License

## 👤 Auteur

RAGEUI

## ⚠️ Avertissement

Cet outil est fourni à des fins éducatives. Assurez-vous de respecter les conditions d'utilisation de Discord et GoFile.
