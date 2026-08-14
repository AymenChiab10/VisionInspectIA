# Scénario de démonstration — VisionInspectIA

Aucun vrai mot de passe n'est écrit dans ce document. Remplacer `[DEMO_EMAIL]` et `[DEMO_PASSWORD]` par les identifiants du compte de démonstration au moment de la préparation, jamais avant.

---

## 1. Préparation avant la démo

- [ ] Vérifier que les trois services Railway sont actifs (backend, frontend, MySQL) — tier gratuit/d'essai, pas de garantie de disponibilité prolongée.
- [ ] Tester `GET https://visioninspectia-production.up.railway.app/` → doit répondre `{"message": "Bottle Defect Detection API", "status": "running", ...}`.
- [ ] Ouvrir `https://frontend-production-bcff.up.railway.app` dans le navigateur qui servira à la démonstration, connexion internet stable vérifiée.
- [ ] Avoir les 4 images de test prêtes localement (voir §3).
- [ ] Avoir `docs/RAPPORT_DE_STAGE.md` et `docs/VisionInspectIA_Soutenance.pptx` ouverts en arrière-plan pour répondre aux questions techniques si besoin.
- [ ] Aucun secret (mot de passe, token) ne doit être visible à l'écran (barre d'adresse, DevTools fermé, gestionnaire de mots de passe du navigateur masqué).

## 2. Démarrage des services (si démo en local plutôt qu'en production)

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (autre terminal)
cd frontend
npm run dev
```

Utiliser la production par défaut ; ne basculer en local qu'en cas de problème réseau (voir Plan B).

## 3. Compte de démonstration

- Email : `[DEMO_EMAIL]`
- Mot de passe : `[DEMO_PASSWORD]`
- Créer ce compte à l'avance via `/register` pour ne pas dépendre de la saisie en direct pendant la démo (le register en direct reste possible comme première étape du scénario si le temps le permet).

## 4. Images à utiliser

Utiliser exclusivement des images déjà validées, issues du dataset de test :

| Classe réelle | Fichier | Résultat attendu (déjà vérifié en production) |
|---|---|---|
| `good` | `data/augmented/bottle/test/good/000.png` | Correct, confiance ≈ 99,4 % |
| `broken_large` | `data/augmented/bottle/test/broken_large/002.png` | Correct, confiance ≈ 99,8 % |
| `broken_small` | `data/augmented/bottle/test/broken_small/002.png` | **Incorrect** — prédit `broken_large`, confiance ≈ 80,5 % (limitation connue, documentée) |
| `contamination` | `data/augmented/bottle/test/contamination/001.png` | Correct, confiance ≈ 99,3 % |

**Sur `broken_small` : ne pas cacher le résultat.** Présenter cette prédiction erronée comme une illustration directe de la limitation documentée au Chapitre 3.16 / 12.4 du rapport, pas comme un échec de la démonstration. C'est le résultat le plus pédagogique de toute la démo.

## 5. Ordre exact des actions

1. **Login** — se connecter avec le compte de démonstration.
2. **Dashboard** — montrer les statistiques actuelles (elles évolueront pendant la démo).
3. **Upload** — importer l'image `good`.
4. **Prediction** — lancer l'analyse, commenter : classe prédite, score de confiance, temps d'inférence affiché.
5. Répéter upload + prediction pour `broken_large`, `broken_small` (résultat honnêtement incorrect), `contamination`.
6. **History** — montrer que les 4 inspections viennent d'apparaître, avec recherche/filtre/tri.
7. **Details** — ouvrir le détail d'une inspection (modal).
8. **PDF** — télécharger et ouvrir le rapport PDF d'une inspection.
9. **CSV** — exporter l'historique et ouvrir le fichier généré.
10. **Dashboard** (retour) — montrer que les statistiques se sont mises à jour avec les 4 nouvelles inspections.
11. **Profile** — montrer l'édition du profil.
12. **Dark mode** — basculer le thème.
13. **Logout**.

## 6. Résultats attendus

- Toutes les étapes 1 à 13 doivent s'enchaîner sans erreur visible dans l'interface.
- Les 4 prédictions doivent correspondre exactement au tableau du §4 (aucune n'a été modifiée ou choisie après coup).
- Les statistiques du dashboard doivent refléter en temps réel les nouvelles inspections (calcul SQL direct, pas de valeur statique).

## 7. Plan B en cas de problème

| Problème | Solution |
|---|---|
| Railway indisponible / lent (tier gratuit) | Basculer en démonstration locale (voir §2) avec la même base MySQL de développement |
| Image de test introuvable | Les 4 fichiers sont aussi présents dans `data/augmented/bottle/test/{classe}/` — reprendre un fichier `00X.png` équivalent de la même classe si le fichier exact manque, en signalant que ce n'est pas l'image exacte déjà validée |
| Prédiction inattendue sur une classe normalement correcte | Ne pas improviser d'explication non vérifiée ; noter le cas et proposer de vérifier après la soutenance plutôt que d'inventer une cause |
| Coupure réseau totale | Utiliser les captures d'écran déjà prises (`docs/screenshots/`) si disponibles, sinon s'appuyer sur le PowerPoint (`docs/VisionInspectIA_Soutenance.pptx`) et le rapport écrit |
| Question sur un point non couvert par la démo | Renvoyer vers `docs/QUESTIONS_JURY.md` ou `docs/RAPPORT_DE_STAGE.md`, ne jamais improviser un chiffre |

## 8. Rappels de sécurité pendant la démo

- Ne jamais afficher `SECRET_KEY`, le mot de passe MySQL, ou un token JWT complet à l'écran.
- Ne jamais ouvrir le dashboard Railway avec les variables d'environnement visibles sans les masquer au préalable.
- Le compte de démonstration ne doit pas être supprimé pendant la démo (fonctionnalité *Delete Account* à montrer, si souhaité, sur un compte jetable créé pour l'occasion, pas le compte principal).
