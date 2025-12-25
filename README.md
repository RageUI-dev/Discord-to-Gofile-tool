# 🚀 Discord to GoFile Uploader

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un outil en ligne de commande performant pour transférer instantanément des fichiers depuis les serveurs CDN de Discord vers **GoFile.io**. 

> **Note :** Cet outil est particulièrement utile pour contourner l'expiration des liens Discord ou pour partager des fichiers volumineux sur une plateforme tierce sans effort.

---

## ✨ Caractéristiques

* **Transfert Direct** : Télécharge depuis Discord et upload vers GoFile de manière fluide.
* **Nettoyage Automatique** : Les fichiers temporaires sont supprimés immédiatement après l'envoi pour préserver votre espace disque.
* **Barre de Progression** : Visualisation en temps réel de l'avancement (pourcentage, Mo téléchargés).
* **Version Exécutable** : Utilisable directement sur Windows sans avoir besoin d'installer Python.
* **Sécurité** : Utilise les serveurs officiels et l'API publique de GoFile.

---

## 🛠️ Installation

### 1. Version Windows (.exe)
* Rendez-vous dans la section **Releases** de ce dépôt.
* Téléchargez le fichier `discord_to_gofile.exe`.
* Double-cliquez pour lancer.

### 2. Version Python (Source)
Si vous souhaitez le lancer manuellement ou si vous êtes sur Linux/Mac :

```bash
# Cloner le dépôt
git clone [https://github.com/VOTRE_NOM/discord-to-gofile.git](https://github.com/VOTRE_NOM/discord-to-gofile.git)
cd discord-to-gofile

# Installer les dépendances nécessaires
pip install requests
