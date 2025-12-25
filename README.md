# Discord to GoFile 🚀

**Discord to GoFile** est un script Python simple et efficace qui permet de télécharger un fichier hébergé sur le CDN de Discord (lien direct) et de l'uploader automatiquement sur GoFile.io, tout en conservant le nom original du fichier. 📁➡️☁️

Idéal pour contourner les limitations de durée des liens Discord ou pour partager des fichiers de manière plus permanente. ⏳🔗

Créé par **RAGEUI** 🔥.

## Fonctionnalités ✨

- 📥 Téléchargement direct depuis les URLs Discord (`cdn.discordapp.com`, `media.discordapp.net`, etc.)
- 📊 Barre de progression détaillée pendant le téléchargement et l'upload
- 🏷️ Conservation du nom de fichier original (avec nettoyage des caractères interdits)
- ⬆️ Upload automatique sur GoFile.io
- 🔗 Affichage clair des résultats avec le lien de téléchargement direct
- 🤫 Mode silencieux (`-q`)
- 🎨 Interface colorée et conviviale en ligne de commande

## Prérequis 🛠️

- Python 3.6 ou supérieur
- Module `requests` (installable via pip)

```bash
pip install requests
