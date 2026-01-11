Video Frame Analyzer

Un petit projet local pour analyser une vidéo en extrayant 1 frame par seconde, calculer la luminosité moyenne de chaque frame, et afficher les résultats dans une interface React.

🗂 Structure du projet
video-frame-analyzer/
├─ backend/
│  ├─ main.py          # API FastAPI pour analyser la vidéo et extraire les frames
│  ├─ venv/            # Environnement virtuel Python
│  └─ videos/          # Vidéos uploadées et frames extraites
├─ frontend/
│  ├─ src/
│  │  ├─ App.js        # Composant principal React
│  │  └─ App.css       # Styles de l'application
│  └─ package.json
└─ README.md

⚡ Fonctionnalités

Upload d’une vidéo depuis le navigateur

Extraction d’1 frame par seconde avec OpenCV

Calcul de la luminosité moyenne pour chaque frame

Sauvegarde des frames en .jpg

Retour d’un JSON complet contenant :

second → seconde de la frame

brightness → luminosité moyenne

frame_url → chemin vers la frame

Affichage des frames dans une grille responsive avec scroll automatique

Affichage du JSON complet pour debug ou analyse

🛠 Prérequis

Python 3.12+

Node.js & npm

Linux / macOS / Windows

Backend Python

FastAPI

OpenCV (opencv-python)

uvicorn

Frontend React

React 18+

npm packages par défaut

🚀 Installation & Lancement
1️⃣ Backend
cd backend
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install --upgrade pip setuptools wheel
pip install fastapi uvicorn opencv-python

# Lancer le serveur
uvicorn main:app --reload


API FastAPI disponible : http://127.0.0.1:8000

2️⃣ Frontend
cd frontend
npm install
npm start


React disponible : http://localhost:3000

📦 Utilisation

Ouvrir l’application React dans le navigateur

Choisir une vidéo locale

Cliquer sur Analyze

Les frames extraites s’affichent en grille avec leur luminosité

Le JSON complet est affiché en dessous pour debug ou récupération des données

🎨 Notes

1 frame par seconde → rapide et léger

Tout fonctionne en local, pas besoin de déploiement

Compatible avec Python 3.12 et OpenCV uniquement

Frontend responsive et scroll automatique

Grille des frames avec hover effet pour une meilleure UX

🔧 Évolution possible

Ajouter calculs supplémentaires : contraste, histogramme, détection d’objets

Filtrer les frames par luminosité ou autre métrique

Ajouter un Dark Mode pour l’interface

Exporter les résultats JSON ou CSV