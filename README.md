# VisionInspectIA

VisionInspectIA est une plateforme web de détection automatique des défauts de bouteilles à partir d'images. Elle combine :

- **Computer Vision** & **Deep Learning** — classification d'images par transfer learning ;
- **MobileNetV2** — modèle retenu à l'issue d'un benchmark comparatif de 4 architectures ;
- **FastAPI** — API REST (authentification JWT, inférence, historique, statistiques, PDF) ;
- **MySQL** — persistance (utilisateurs, historique des inspections) ;
- **React** — interface web moderne, responsive, avec dashboard et graphiques.

Un utilisateur authentifié peut importer la photo d'une bouteille, obtenir en quelques dizaines de millisecondes une prédiction automatique de son état (`good`, `broken_large`, `broken_small`, `contamination`), consulter l'historique de ses inspections, suivre des statistiques sur un dashboard, et générer un rapport PDF ou exporter son historique en CSV.

## Features

### Authentication
- Register / Login / Logout (JWT Bearer)
- Edit profile
- Change password
- Delete account (suppression en cascade : compte, inspections, images)

### AI Inspection
- Upload d'image (drag & drop ou sélection)
- Aperçu de l'image avant analyse
- Prédiction MobileNetV2
- Score de confiance
- Temps d'inférence affiché
- 4 classes de défaut : `good`, `broken_large`, `broken_small`, `contamination`

### History
- Historique des inspections
- Recherche
- Filtres (par classe, par période)
- Tri (plus récent, plus ancien, confiance)
- Pagination
- Détail d'une inspection (modal)
- Suppression d'une inspection (image + ligne base supprimées ensemble)

### Dashboard
- Total des inspections
- Répartition par classe
- Statistiques de confiance (moyenne, la plus haute, la plus basse)
- Graphiques (répartition, barres)
- Évolution des inspections dans le temps
- Galerie des dernières inspections

### Reports
- Rapport PDF par inspection (généré en mémoire, sans fichier temporaire)
- Export CSV de l'historique

### UX
- Dark mode (mémorisé dans le navigateur)
- Centre de notifications
- Interface responsive (desktop / tablette / mobile)

## Architecture

```text
React Frontend (Vite)
      |
      | REST API / JWT
      ↓
FastAPI Backend
      |
      +------ MySQL (utilisateurs, historique)
      |
      +------ MobileNetV2 (modele charge une seule fois, en memoire)
                 |
                 ↓
              Prediction (classe + confiance + temps d'inference)
```

Le backend est organisé en couches simples : `api/` (routes HTTP) → `services/` (logique métier) → `models/` (tables SQLAlchemy) / `ml/` (chargement et inférence du modèle, isolé du pipeline d'entraînement). Le frontend suit la même logique de séparation : `api/` (appels HTTP centralisés) → `context/`+`hooks/` (état global : auth, thème, notifications) → `components/` → `pages/`.

## Technologies utilisées

| Domaine | Technologie |
|---|---|
| Frontend | React 18 (Vite), React Router DOM, Axios, Recharts, lucide-react, Context API |
| Backend | FastAPI, Uvicorn, Pydantic |
| Intelligence artificielle | TensorFlow / Keras, MobileNetV2 (transfer learning) |
| Base de données | MySQL, SQLAlchemy (ORM), Alembic (configuré, prêt pour de futures migrations) |
| Authentification | JWT (python-jose), hachage bcrypt (passlib) |
| Rapports | ReportLab (PDF), export CSV natif (sans dépendance) |

## Installation

### Prérequis

- Python 3.11+ (développé et testé avec Python 3.13)
- Node.js 18+ (développé et testé avec Node 22)
- Un serveur MySQL (développé et testé avec MariaDB via XAMPP)

### Base de données

Créer une base vide nommée `visioninspectia` :

```sql
CREATE DATABASE IF NOT EXISTS visioninspectia CHARACTER SET utf8mb4;
```

Les tables (`users`, `inspections`) sont créées automatiquement au démarrage du backend (voir `app/db/init_db.py`) — aucune commande SQL manuelle supplémentaire n'est nécessaire.

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Editer .env : renseigner DATABASE_USER / DATABASE_PASSWORD / SECRET_KEY (une valeur aleatoire, jamais la valeur par defaut)
```

Variables d'environnement (`backend/.env`) :

```
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=visioninspectia
DATABASE_USER=root
DATABASE_PASSWORD=

SECRET_KEY=<a generer, ex: python -c "import secrets; print(secrets.token_hex(32))">
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
```

Variable d'environnement (`frontend/.env`) :

```
VITE_API_URL=http://localhost:8000/api/v1
```

## Lancement

### Backend

```bash
cd backend
uvicorn app.main:app --reload
```

- API : http://localhost:8000
- Documentation interactive (Swagger) : http://localhost:8000/docs
- Documentation ReDoc : http://localhost:8000/redoc

Au démarrage, le modèle MobileNetV2 est chargé une seule fois en mémoire (`MobileNetV2 loaded successfully` dans les logs) et n'est jamais rechargé par la suite.

### Frontend

```bash
cd frontend
npm run dev
```

- Application : http://localhost:5173

Le backend n'autorise, en CORS, que l'origine `http://localhost:5173` (configuration par défaut de Vite).

## Structure du projet

```
VisionInspectIA/
├── ai/            # Pipeline de recherche : preparation du dataset, entrainement,
│                  # benchmark de 4 modeles, modele final retenu (mobilenet_v2)
├── backend/       # API REST FastAPI (auth, prediction, historique, dashboard, PDF, CSV)
├── frontend/      # Application React (Vite) consommant l'API
├── data/          # Dataset MVTec AD brut, traite et augmente (non versionne, volumineux)
└── database/, docs/, reports/  # Repertoires reserves, non utilises dans cette version
```

- **`ai/`** — Code de recherche et d'entraînement, indépendant de l'application web. Contient la configuration du dataset (`ai/config`), les architectures de modèles (`ai/models`), les scripts de préparation/augmentation/entraînement (`ai/scripts`, `ai/training`) et les résultats du benchmark (`ai/results`). Le fichier `ai/saved_models/mobilenet_v2/best_model.keras` est le seul artefact réutilisé par le backend.
- **`backend/`** — API en couches simples : `api/` (routes HTTP), `services/` (logique métier), `models/` (tables SQLAlchemy), `schemas/` (validation Pydantic), `ml/` (chargement du modèle et inférence, isolé du pipeline d'entraînement), `db/` (connexion MySQL), `core/` (configuration et sécurité).
- **`frontend/`** — Application React : `api/` (appels HTTP centralisés), `context/` + `hooks/` (authentification, thème, notifications), `components/` (éléments réutilisables), `pages/` (écrans), `routes/` (routage et protection des pages privées).

## Résultats IA — Benchmark des modèles

Benchmark réalisé sur le dataset augmenté équilibré (800 images d'entraînement / 160 validation / 160 test, 200/40/40 par classe), conditions expérimentales strictement identiques pour les 4 modèles (mêmes hyperparamètres, callbacks, preprocessing). Résultats mesurés et vérifiés (`ai/results/benchmark_results.json`) :

| Modèle | Accuracy | F1-score (macro) | Temps d'inférence |
|---|---|---|---|
| **MobileNetV2 (retenu)** | **75,63 %** | **0,738** | **9,05 ms** |
| ResNet50 | 78,13 % | 0,772 | 23,70 ms |
| EfficientNetB0 | 71,25 % | 0,688 | 11,45 ms |
| CNN personnalisé (from scratch) | 25,00 % | 0,100 | 7,44 ms |

### Pourquoi MobileNetV2 a été retenu

- **Transfer learning décisif** : les trois modèles pré-entraînés sur ImageNet (MobileNetV2, EfficientNetB0, ResNet50) surclassent de 46 à 53 points le CNN entraîné from scratch, qui ne dépasse jamais le niveau du hasard (25 % sur 4 classes) faute de données réelles suffisantes (10 à 15 photos sources par classe de défaut).
- **Meilleur compromis global, pas le meilleur score brut** : ResNet50 obtient l'accuracy la plus haute (78,13 % contre 75,63 %), mais cet écart de 2,5 points n'est pas statistiquement robuste — le jeu de test ne contient que 5 à 6 images sources réellement uniques par classe de défaut (le reste étant des copies), rendant un tel écart comparable au bruit d'échantillonnage.
- **Coût de déploiement très inférieur** : MobileNetV2 est 10× plus léger que ResNet50 (9,24 Mo contre 90,71 Mo), 2,6× plus rapide à l'inférence (9,05 ms contre 23,70 ms) et 2,6× plus rapide à ré-entraîner — des facteurs directement pertinents pour l'intégration dans une application web sans infrastructure GPU dédiée.
- **Conclusion** : à performance quasi équivalente, MobileNetV2 offre le meilleur rapport performance / robustesse / coût / facilité d'intégration.

## Validation finale

Tests exécutés en conditions réelles (backend + MySQL + frontend build), lors de la validation finale du projet :

| Test | Résultat |
|---|---|
| Prédiction sur 4 images de démonstration (une par classe, labels connus) | ✅ 4/4 correctes |
| Backend (démarrage, `/`, `/docs`, `/redoc`, modèle chargé une seule fois) | ✅ |
| MySQL (schéma, clés, contraintes) | ✅ |
| Authentification (register/login/me/logout + cas d'erreur) | ✅ |
| Historique (création, détail, suppression avec fichier + ligne base) | ✅ |
| Dashboard (cohérence avec les données réelles de MySQL) | ✅ |
| PDF (contenu vérifié : utilisateur, date, classe, confiance, image) | ✅ |
| CSV (génération vérifiée sur données réelles, réouverte avec un parseur CSV) | ✅ |
| Profil (édition, changement de mot de passe, suppression de compte en cascade) | ✅ |
| Sécurité (accès sans JWT, JWT invalide, accès aux données d'un autre utilisateur) | ✅ |
| Build frontend (`npm run build`) | ✅ 0 erreur |

> Note : la vérification visuelle du rendu (dark mode, responsive, apparence générale) nécessite un navigateur réel et reste à confirmer manuellement — non exécutable dans l'environnement de développement utilisé pour ces tests automatisés.

## Limitations connues

- **Rareté des données réelles** : le dataset MVTec AD *bottle* ne contient que 20 à 22 images réelles par classe de défaut. Le rappel du modèle retenu sur la classe `broken_small` n'est que de 50 %, un défaut subtil parfois confondu avec `broken_large` ou `good`.
- **Classe `contamination`** également plus difficile (rappel ~53 %), le modèle ayant tendance à la confondre avec `good` en cas d'ambiguïté visuelle — le risque le plus critique en contrôle qualité (un défaut réel classé "bon").
- **Pas de fine-tuning** : le backbone MobileNetV2 est resté entièrement gelé (feature extraction uniquement) ; un fine-tuning des dernières couches pourrait améliorer la détection des défauts les plus subtils, au prix d'un temps d'entraînement plus long.
- **Base de test peu diversifiée** : plusieurs classes de test ne reposent que sur 3 à 6 images sources uniques (dupliquées pour atteindre 40 images/classe), ce qui limite la significativité statistique des métriques par classe.
- **Stockage des images uploadées non persistant en production** : sur Railway, le système de fichiers du conteneur backend est éphémère — une image uploadée reste accessible pendant la durée de vie du déploiement, mais est perdue au prochain redéploiement (build, changement de variable d'environnement, etc.). La ligne correspondante reste en base (historique, statistiques), seule l'image et la génération du PDF avec image sont affectées. Non bloquant pour une démonstration de stage ; nécessiterait un volume persistant ou un stockage objet (S3-compatible) pour une utilisation prolongée.

## Deployment

Déploiement réel sur [Railway](https://railway.app), retenu car seule plateforme testée (Render, Railway, Hugging Face Spaces) à proposer une base MySQL managée nativement, permettant d'héberger backend, frontend et base de données sur une seule plateforme.

### Frontend
URL : https://frontend-production-bcff.up.railway.app

### Backend
URL : https://visioninspectia-production.up.railway.app

### API Documentation
Swagger : https://visioninspectia-production.up.railway.app/docs
ReDoc : https://visioninspectia-production.up.railway.app/redoc

### Database
MySQL managé par Railway (plugin officiel), accessible uniquement depuis le réseau privé du projet (non exposée publiquement). Tables créées automatiquement au démarrage du backend (`init_db()`, appelé depuis `app/main.py`).

### Environment variables
Définies dans le service Railway (jamais commitées) : `DATABASE_HOST/PORT/USER/PASSWORD/NAME` (référencées depuis le plugin MySQL), `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `DEBUG=False`, `CORS_ORIGINS` (URL du frontend), et `VITE_API_URL` côté frontend (passée comme build arg Docker, l'URL de l'API étant figée au moment du build par Vite). Voir `backend/.env.example` pour la liste complète avec description.

### Local development
Voir les sections [Installation](#installation) et [Lancement](#lancement) ci-dessus — inchangées, le développement local n'utilise ni Railway ni Docker.

### Production deployment
Backend et frontend sont chacun déployés comme un service Railway séparé à partir du même dépôt GitHub (`Root Directory` = `backend/` ou `frontend/` selon le service), chacun avec son propre `Dockerfile` (`backend/Dockerfile`, `frontend/Dockerfile`). Le backend embarque sa propre copie du modèle MobileNetV2 (`backend/app/ml/model_files/`), rendant son déploiement indépendant du dossier `ai/`. Le frontend est buildé (`npm run build`) puis servi en statique (`serve -s dist`).

### Troubleshooting
- **"Table doesn't exist" au premier déploiement** : vérifier que `init_db()` est bien appelé au démarrage (`app/main.py`, fonction `lifespan`) et que les variables `DATABASE_*` pointent vers la bonne base.
- **Erreur CORS dans la console navigateur** : vérifier que `CORS_ORIGINS` sur le backend contient exactement l'URL du frontend déployé (sans `/` final), et redéployer le backend après modification.
- **Frontend appelle `localhost:8000` en production** : `VITE_API_URL` n'était pas définie au moment du `npm run build` — Vite fige cette valeur dans le bundle, la redéfinir après coup ne suffit pas, il faut redéclencher un build.
- **Image d'une inspection introuvable (404 sur `/uploads/...`)** : comportement attendu après un redéploiement du backend, voir la limitation « stockage non persistant » ci-dessus.
- **Build backend très long / échoue par manque de mémoire** : `tensorflow` est une dépendance lourde ; s'assurer que le plan Railway utilisé dispose de suffisamment de RAM pour l'installation et le chargement du modèle.
