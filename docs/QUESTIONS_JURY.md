# Questions/réponses anticipées — Soutenance VisionInspectIA

Préparé à partir du contenu vérifié de `docs/RAPPORT_DE_STAGE.md`, `docs/TECHNICAL_DOCUMENTATION.md` et des fichiers réels du projet. Aucune réponse n'invente une information absente des sources — les points non vérifiables sont marqués explicitement.

---

## IA

**1. Pourquoi MobileNetV2 et pas ResNet50, qui a une meilleure accuracy ?**
ResNet50 obtient une accuracy légèrement supérieure (78,13 % contre 75,63 %), mais MobileNetV2 a été retenu comme meilleur **compromis** : F1-score macro proche (0,742 contre 0,772), modèle 10 fois plus léger (9,24 Mo contre 90,71 Mo) et 2,6 fois plus rapide à l'inférence (9,16 ms contre 23,70 ms). Dans un contexte de déploiement web sans GPU dédié, ce compromis a été jugé plus pertinent qu'un gain d'accuracy de 2,5 points, d'autant que le jeu de test repose sur peu d'images sources uniques (voir Q7).

**2. Pourquoi 224×224 en entrée du modèle ?**
C'est la taille d'entrée standard des architectures pré-entraînées sur ImageNet utilisées (MobileNetV2, EfficientNetB0, ResNet50), permettant de réutiliser directement leurs poids pré-entraînés en transfer learning.

**3. Pourquoi ces quatre classes précisément ?**
Ce sont les classes fournies par le dataset MVTec AD pour la catégorie *bottle* : une classe conforme (`good`) et trois classes de défaut (`broken_large`, `broken_small`, `contamination`).

**4. Comment avez-vous préparé les données ?**
Le dataset brut (292 images, MVTec AD) a été analysé (formats, doublons, intégrité — aucun problème détecté), puis augmenté par duplication et transformations (RandomFlip, RandomRotation, RandomZoom, RandomBrightness) pour équilibrer les quatre classes à 200 images en entraînement et 40 en test.

**5. Comment avez-vous évité la fuite de données (data leakage) ?**
Un problème a été identifié : compléter la validation par duplication (comme le test) risquait d'introduire des images quasi identiques entre train et validation, biaisant l'early stopping. La correction retenue construit la validation exclusivement à partir d'images réelles uniques, sans duplication, quitte à obtenir moins d'images que la cible. Ce choix est documenté explicitement dans le code (`ai/scripts/data_augmentation.py`).

**6. Pourquoi le modèle échoue-t-il sur `broken_small` ?**
Le rappel sur cette classe n'est que de 0,5 (confondue avec `broken_large`), très probablement à cause du faible nombre d'images sources réelles disponibles (22 images brutes au total pour cette classe, réparties entre validation et test). C'est une limitation assumée et documentée, confirmée à nouveau lors d'un test en production.

**7. Le jeu de test est-il fiable, vu qu'il est en partie dupliqué ?**
Le jeu de test ne repose que sur 3 à 6 images sources réellement uniques par classe, le reste étant obtenu par augmentation. Cela limite la portée statistique des écarts fins entre modèles (ex. les 2,5 points entre MobileNetV2 et ResNet50), mais reste représentatif pour départager un modèle proche du hasard (le CNN from scratch, 25 % d'accuracy) des modèles pré-entraînés.

**8. Qu'est-ce que le domain shift, et l'avez-vous testé ?**
Le domain shift désigne la perte de performance d'un modèle face à des données différentes de son domaine d'entraînement (autre éclairage, autre fond, autre appareil photo). Il n'a **pas** été évalué dans ce projet : tous les tests, y compris en production, utilisent des images issues du même dataset MVTec AD que celui de l'entraînement. C'est une limitation explicitement documentée, pas une performance en conditions industrielles réelles.

**9. Pourquoi augmenter le dataset plutôt que d'utiliser les données brutes ?**
Le dataset brut ne fournit que 20 à 22 images par classe de défaut (et aucune image de défaut en entraînement, MVTec AD ne fournissant que des images `good` dans son split train). Sans augmentation, l'entraînement d'un modèle à 4 classes équilibrées aurait été impossible.

**10. Le modèle a-t-il été fine-tuné ?**
Non. Le protocole utilisé est le *feature extraction* : le backbone pré-entraîné est gelé (`trainable=False`), seule la tête de classification est entraînée. Le fine-tuning du backbone est cité comme perspective, non réalisé.

---

## Backend

**11. Pourquoi FastAPI plutôt que Flask ?**
FastAPI a été retenu parmi les deux options du cahier des charges pour sa validation de données native (Pydantic), sa documentation interactive générée automatiquement (Swagger/ReDoc), et son support natif de l'asynchrone.

**12. Pourquoi SQLAlchemy et pourquoi MySQL ?**
SQLAlchemy est l'ORM Python standard, offrant une abstraction propre au-dessus de MySQL. MySQL a été imposé par le cahier des charges du stage.

**13. Comment fonctionne l'authentification JWT ?**
À la connexion, le backend vérifie le mot de passe (haché avec bcrypt) puis émet un jeton JWT (HS256) avec une durée de validité configurable. Ce jeton est fourni dans l'en-tête `Authorization: Bearer <token>` à chaque requête protégée, vérifié côté serveur par une dépendance FastAPI (`get_current_user`).

**14. Comment protégez-vous les données entre utilisateurs ?**
Chaque requête portant sur des inspections filtre systématiquement sur l'identifiant de l'utilisateur authentifié (extrait du JWT, jamais d'un paramètre client). Vérifié en production : l'accès à l'inspection ou au PDF d'un autre utilisateur retourne 404, sans révéler l'existence de la ressource.

**15. Que se passe-t-il si un utilisateur supprime son compte ?**
Le compte, ses inspections et les fichiers image associés sont supprimés. Ce n'est pas une contrainte SQL `ON DELETE CASCADE` mais une suppression orchestrée par la logique applicative (`user_service.py`).

---

## Frontend

**16. Pourquoi React plutôt qu'Angular ?**
React a été retenu parmi les deux options proposées par le cahier des charges.

**17. Pourquoi Vite ?**
Vite est l'outil de build standard pour React aujourd'hui, offrant un démarrage et un rechargement à chaud rapides en développement.

**18. Comment fonctionne l'upload d'image ?**
L'image est envoyée en `multipart/form-data` vers `POST /predictions/predict`, avec le JWT en en-tête. Le backend valide le format et la taille avant tout traitement.

**19. Comment les résultats sont-ils affichés ?**
Le frontend reçoit un JSON (classe prédite, score de confiance, temps d'inférence) et l'affiche dans l'interface. [Le rendu visuel exact n'a pas pu être vérifié dans un navigateur réel dans l'environnement de développement utilisé — voir Q20.]

**20. L'interface a-t-elle été testée visuellement (dark mode, responsive) ?**
Non, explicitement. L'environnement de développement utilisé ne dispose pas de navigateur graphique. Les fonctionnalités (dark mode, responsive, notifications) sont implémentées dans le code mais leur rendu réel n'a jamais été vérifié visuellement — c'est une limitation assumée du rapport, pas une omission cachée.

---

## Déploiement

**21. Pourquoi Railway et pas Render ou Hugging Face Spaces ?**
Railway est la seule des trois plateformes du cahier des charges à proposer une base MySQL managée nativement (Render n'a pas de MySQL managé ; Hugging Face Spaces n'est pas conçu pour une app full-stack avec authentification et base relationnelle).

**22. Comment les services communiquent-ils en production ?**
Le frontend appelle le backend en HTTPS/REST, avec CORS restreint à l'origine exacte du frontend déployé (pas de wildcard). Le backend communique avec MySQL exclusivement via le réseau privé Railway, non exposé publiquement.

**23. Comment les variables secrètes sont-elles gérées ?**
Toutes (SECRET_KEY, mot de passe MySQL, etc.) sont définies comme variables d'environnement au niveau de chaque service Railway, jamais commitées dans le dépôt Git. `backend/.env.example` ne contient que des placeholders.

**24. Quelles sont les limitations du stockage en production ?**
Le système de fichiers du conteneur backend Railway est éphémère : une image uploadée est accessible pendant la durée de vie du déploiement mais perdue au redéploiement suivant. Confirmé par test réel. Les données en base (historique, statistiques) ne sont pas affectées ; seule l'image et l'affichage image dans le PDF le sont.

**25. Le déploiement s'est-il bien passé du premier coup ?**
Non. Plusieurs problèmes réels ont été rencontrés et documentés : échec du builder automatique Railpack sur la structure en monorepo, dépendance initiale du backend au dossier `ai/` (corrigée en rendant le backend autonome), erreur de gestion de la variable `$PORT`, configuration figée lors d'un simple redéploiement, et absence d'appel à `init_db()` au démarrage (tables inexistantes sur une base neuve). Chaque problème et sa correction sont détaillés au Chapitre 10 du rapport.

---

## Architecture

**26. Pourquoi séparer frontend et backend plutôt qu'un monolithe ?**
Cela permet un déploiement, une mise à l'échelle et une évolution indépendants de l'interface et de l'API, et correspond à l'architecture demandée par le cahier des charges (frontend/backend/base de données distincts).

**27. Comment circule une requête de prédiction, de bout en bout ?**
Upload (frontend) → validation du fichier (backend) → sauvegarde disque → prétraitement (224×224) → inférence MobileNetV2 → enregistrement MySQL → réponse JSON (classe, confiance, temps d'inférence) → affichage frontend.

**28. Où est chargé le modèle IA ? Est-ce un service séparé ?**
Non, le modèle est chargé directement en mémoire dans le processus du service backend FastAPI, pas dans un service distinct.

**29. Pourquoi le modèle n'est-il chargé qu'une seule fois ?**
Le chargement d'un modèle TensorFlow est coûteux (plusieurs secondes). Il est donc chargé une seule fois au démarrage du serveur (fonction `lifespan`), puis réutilisé pour toutes les requêtes suivantes — d'où le *cold start* observé uniquement sur le tout premier appel.

**30. Quelle est la différence entre le temps d'inférence du benchmark (~9 ms) et le temps observé en production (170–210 ms) ?**
Le temps d'inférence du benchmark ne mesure que l'appel `model.predict()` sur une image déjà prétraitée, modèle déjà chargé. Le temps observé en production est le temps HTTP complet : upload réseau, validation, prétraitement, inférence, écriture MySQL et réponse — d'où l'écart.
