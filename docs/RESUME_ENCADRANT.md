# VisionInspectIA — Résumé pour l'encadrant

**Objectif.** Automatiser la détection de défauts sur des bouteilles à partir d'une photo, via une plateforme web complète : upload, classification par intelligence artificielle, historique, statistiques et rapports.

**Stack.** React (Vite) · FastAPI · MySQL (SQLAlchemy) · TensorFlow / Keras (MobileNetV2) · JWT · ReportLab (PDF) · Recharts.

## Ce qui est implémenté

- **Authentification complète** : inscription, connexion, déconnexion, JWT, modification du profil, changement de mot de passe, suppression de compte (avec suppression en cascade des inspections et images associées).
- **Inspection IA** : upload par drag & drop, aperçu, prédiction MobileNetV2 sur 4 classes (`good`, `broken_large`, `broken_small`, `contamination`), score de confiance, temps d'inférence affiché.
- **Historique** : liste, recherche, filtres, tri, pagination, détail, suppression.
- **Dashboard** : statistiques agrégées (total, répartition par classe, confiance moyenne), graphiques (répartition, barres, évolution), galerie des dernières inspections — toutes calculées en direct depuis MySQL.
- **Rapports** : PDF généré en mémoire (ReportLab), export CSV généré côté client.
- **UX** : dark mode, notifications, interface responsive.
- **Sécurité** : mots de passe hashés (bcrypt), isolation stricte des données entre utilisateurs, gestion explicite des erreurs 401/404/400.

## Résultats du modèle IA (jeu de test, 160 images, 40/classe)

| Modèle retenu | Accuracy | F1 macro | Taille | Inférence |
|---|---|---|---|---|
| **MobileNetV2** | 75,63 % | 0,742 | 9,24 MB | ~9 ms |

MobileNetV2 a été retenu, dans les conditions expérimentales du projet, comme meilleur compromis entre performance, taille et vitesse face à ResNet50, EfficientNetB0 et un CNN entraîné from scratch (benchmark détaillé dans `docs/TECHNICAL_DOCUMENTATION.md`, §3).

## Tests réalisés

Backend, MySQL, authentification, prédiction, historique, dashboard, PDF, CSV, gestion du profil et sécurité ont tous été testés en conditions réelles (API réelle, base MySQL réelle). Flux de bout en bout : 28/28 vérifications réussies. Build frontend : 0 erreur. Le seul échec connu dans la suite de tests hérités concerne une limitation de reconnaissance du modèle sur `broken_small`, pas un bug logiciel.

**Non vérifié à ce stade :** le rendu visuel de l'interface (dark mode, responsive) dans un navigateur réel — l'environnement de développement utilisé ne dispose pas de navigateur.

## Limites connues

- Jeu de test reposant sur un nombre restreint d'images sources réellement uniques par classe.
- Difficulté persistante sur la classe `broken_small` (rappel 50 %).
- Généralisation limitée à des images hors du domaine d'entraînement.
- Pas encore de validation sur de vraies photos prises en conditions de production réelles.
- Alembic configuré mais aucune migration versionnée à ce jour.

## Perspectives

Enrichissement du dataset réel, amélioration ciblée sur `broken_small`, tests en conditions réelles supplémentaires, robustesse au domain-shift, détection out-of-distribution, optimisation du bundle frontend, migrations Alembic complètes, déploiement cloud.

Le système est fonctionnel et validé techniquement dans un cadre de démonstration ; il n'est pas présenté comme prêt pour un déploiement en production.
