# Discord to GoFile

Transfert rapide de fichiers Discord CDN vers GoFile.

## Installation

```bash
pip install requests
```

## Utilisation

```bash
python discord_to_gofile.py
```

Ou directement avec l'URL :

```bash
python discord_to_gofile.py "https://cdn.discordapp.com/attachments/..."
```

## Options

```bash
-q, --quiet      Mode silencieux
--no-pause       Pas de pause à la fin
```

## Exemple

```bash
python discord_to_gofile.py -q "https://cdn.discordapp.com/attachments/123/456/file.zip"
```

## Fonctionnalités

- Barre de progression
- Préservation du nom de fichier
- Gestion des erreurs
- Nettoyage automatique

---

**Made by RAGEUI**
