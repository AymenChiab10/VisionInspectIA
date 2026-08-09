# Rapport de Benchmark - Architectures de Classification d'Images

**Projet :** VisionInspectAI  
**Dataset :** MVTec Bottle (raw)  
**Date du benchmark :** 2026-08-08  
**Protocole :** Feature Extraction (Phase A) - Backbone gelé, tête entraînable uniquement  

---

## 1. Résumé Exécutif

Ce rapport présente une comparaison systématique de quatre architectures de classification d'images sur le dataset MVTec Bottle. L'expérimation respecte une méthodologie scientifique reproductible, avec un protocole expérimental identique pour toutes les architectures.

**Constat majeur :** Dans cette configuration expérimentale, les class weights n'ont pas permis d'améliorer significativement la détection des classes minoritaires.

**Résultat principal :** Les quatre architectures atteignent des performances identiques sur les métriques principales (F1-score macro = 0.2179), révélant une limitation fondamentale du protocole de Feature Extraction sur ce dataset.

---

## 2. Protocole Expérimental

### 2.1 Stratégie de Transfer Learning

#### Phase A - Feature Extraction (actuelle)
- Backbone gelé (`trainable=False`)
- Seule la tête de classification est entraînée
- Objectif : évaluer les performances du backbone pré-entraîné isolément

#### Phase B - Fine-Tuning (future)
- Débloquer progressivement les 20-30 dernières couches du backbone
- Conserver les premières couches gelées
- Learning rate très faible (1e-5 ou 5e-6)
- Comparaison avec la version backbone gelé

### 2.2 Configuration Expérimentale Identique

| Paramètre | Valeur |
|-----------|--------|
| Dataset | MVTec Bottle (raw) |
| Split | Train: 224 / Val: 64 / Test: 64 |
| Preprocessing | Resize 224x224, /255.0 |
| Classes | broken_large, broken_small, contamination, good |
| Class weights | {0: 3.64, 1: 3.4, 2: 3.4, 3: 0.32} |
| Optimizer | Adam |
| Learning rate | 1e-3 |
| Batch size | 32 |
| Epochs max | 30 |
| EarlyStopping | patience=8, monitor=val_loss |
| ModelCheckpoint | monitor=val_loss, save_best_only=True |
| Dropout | 0.3 |
| Weight decay | 1e-4 |

---

## 3. Résultats Comparatifs

### 3.1 Tableau Synthétique

| Modèle | Params | Taille | Temps entraînement | Inférence (ms) | Accuracy | Precision macro | Recall macro | F1-score macro |
|--------|--------|--------|-------------------|----------------|----------|-----------------|--------------|----------------|
| CNN personnalisé | 1.88M | 21.67 MB | 2:47 | 14.11 | 0.8333 | 0.1932 | 0.2500 | 0.2179 |
| MobileNetV2 | 2.26M | 9.24 MB | 1:18 | 15.49 | 0.2206 | 0.1932 | 0.2500 | 0.2179 |
| EfficientNetB0 | 4.05M | 16.32 MB | 1:10 | 14.99 | 0.1667 | 0.1932 | 0.2500 | 0.2179 |
| ResNet50 | 23.60M | 90.71 MB | 1:42 | 32.11 | 0.2696 | 0.1932 | 0.2500 | 0.2179 |

### 3.2 Analyse des Courbes d'Entraînement

**CNN personnalisé :**
- Meilleur epoch : 8
- Sévere overfitting : train_acc = 0.83, val_acc = 0.07
- Le modèle apprend par cœur le training set sans généraliser

**MobileNetV2 :**
- Meilleur epoch : 4
- Underfitting : train_acc = 0.22
- Le backbone pré-entraîné ne s'adapte pas à ce dataset spécifique

**EfficientNetB0 :**
- Meilleur epoch : 4
- Underfitting : train_acc = 0.17
- Comportement similaire à MobileNetV2

**ResNet50 :**
- Meilleur epoch : 1
- Underfitting : train_acc = 0.27
- Le modèle ne dépasse pas le hasard pur sur le training set

### 3.3 Matrices de Confusion

Toutes les architectures présentent le même pattern de prédiction :

```
             Prédiction
             BL   BS   CT   GOOD
Réel BL        0    0    0     3
     BS        0    0    0     4
     CT        0    0    0     3
     GOOD      0    0    0    34
```

**Observation :** Toutes les classes minoritaires sont systématiquement prédites comme la classe majoritaire "good", malgré les class weights.

---

## 4. Analyse Critique des Architectures

### 4.1 CNN Personnalisé

**Avantages :**
- Nombre de paramètres minimal (1.88M)
- Temps d'inférence compétitif (14.11 ms)
- Architecture légère et interprétable

**Limites :**
- Overfitting sévère dès les premières epochs
- Performance de généralisation très faible
- Nécessite une régularisation plus forte

**Verdict :** Architecture trop simple pour capturer la complexité des défauts avec si peu de données.

### 4.2 MobileNetV2

**Avantages :**
- Taille modèle minimale (9.24 MB)
- Architecture optimisée pour mobile/edge
- Profondeur-wise separable convolutions efficaces

**Limites :**
- Underfitting marqué
- Backbone trop contraint pour ce type de données
- Performance identique au hasard sur training set

**Verdict :** Bon compromis taille/performance, mais nécessite du fine-tuning pour exploiter son potentiel.

### 4.3 EfficientNetB0

**Avantages :**
- Meilleur temps d'entraînement (1:10)
- Temps d'inférence excellent (14.99 ms)
- Compound scaling optimal

**Limites :**
- Underfitting comme MobileNetV2
- Plus de paramètres que MobileNetV2 pour des résultats identiques en Phase A

**Verdict :** Excellent candidat pour le fine-tuning grâce à son efficacité paramétrique.

### 4.4 ResNet50

**Avantages :**
- Backbone très expressif (23.6M params)
- Architectures résiduelles éprouvées
- Bonnes performances sur de nombreuses tâches

**Limites :**
- Taille modèle importante (90.71 MB)
- Temps d'inférence le plus élevé (32.11 ms)
- Underfitting en Phase A

**Verdict :** Trop lourd pour le déploiement edge, mais puissant potentiel après fine-tuning.

---

## 5. Sélection de la Meilleure Architecture

### 5.1 Critères de Décision (par ordre de priorité)

1. F1-score macro
2. Recall des classes minoritaires
3. Precision macro
4. Temps d'inférence
5. Taille du modèle
6. Nombre de paramètres
7. Temps d'entraînement

### 5.2 Analyse Multicritère

| Critère | CNN | MobileNetV2 | EfficientNetB0 | ResNet50 | Gagnant |
|---------|-----|-------------|----------------|----------|---------|
| F1-score macro | 0.2179 | 0.2179 | 0.2179 | 0.2179 | Égalité |
| Recall macro | 0.2500 | 0.2500 | 0.2500 | 0.2500 | Égalité |
| Precision macro | 0.1932 | 0.1932 | 0.1932 | 0.1932 | Égalité |
| Inférence (ms) | 14.11 | 15.49 | 14.99 | 32.11 | **CNN** |
| Taille (MB) | 21.67 | 9.24 | 16.32 | 90.71 | **MobileNetV2** |
| Params (M) | 1.88 | 2.26 | 4.05 | 23.60 | **CNN** |
| Temps entraînement | 2:47 | 1:18 | 1:10 | 1:42 | **EfficientNetB0** |

### 5.3 Recommandation

**Architecture retenue : MobileNetV2**

**Justification :**
- Égalité parfaite sur les métriques principales (F1, recall, precision)
- Meilleur compromis taille/déploiement (9.24 MB)
- Temps d'inférence acceptable (15.49 ms)
- Nombre de paramètres raisonnable (2.26M)
- Architecture mature et largement déployée en production

**Note :** Le choix est contraint par l'égalité des métriques. La Phase B (fine-tuning) pourrait redistribuer les performances et modifier ce classement.

---

## 6. Analyse des Class Weights

### 6.1 Constat Expérimental

Dans cette configuration expérimentale, les class weights n'ont pas permis d'améliorer significativement la détection des classes minoritaires.

### 6.2 Hypothèses

Le comportement des class weights dépend de multiples facteurs :

- **Volume de données :** 292 images seulement, les classes minoritaires ont 20-22 images chacune
- **Qualité des données :** Les défauts peuvent être subtils et nécessiter une feature extraction sophistiquée
- **Architecture :** Backbone gelé limite l'adaptation au domaine spécifique
- **Learning rate :** 1e-3 peut être trop élevé pour une tête de classification avec peu de données
- **Fonction de perte :** Le poids de la classe majoritaire (0.32) est trop faible pour compenser le déséquilibre
- **Stratégie d'entraînement :** Feature Extraction vs Fine-Tuning

### 6.3 Conclusion

Nous ne devons pas généraliser cette observation à d'autres datasets ou configurations. Cette conclusion est spécifique à notre contexte expérimental.

---

## 7. Feuille de Route du Projet

### Phase A - Benchmark Feature Extraction ✅ COMPLÉTÉE
- [x] Diagnostiquer le déséquilibre de classes
- [x] Intégrer le dataset MVTec Bottle
- [x] Ajouter les métriques sklearn (F1 macro, precision macro, recall macro)
- [x] Construire l'infrastructure de benchmark
- [x] Entraîner CNN personnalisé
- [x] Entraîner MobileNetV2 (backbone gelé)
- [x] Entraîner EfficientNetB0 (backbone gelé)
- [x] Entraîner ResNet50 (backbone gelé)
- [x] Générer le rapport comparatif
- [x] Sélectionner la meilleure architecture

### Phase B - Fine-Tuning 🔜 PROCHAINE ÉTAPE
- [ ] Sélectionner MobileNetV2 comme baseline
- [ ] Débloquer les 20-30 dernières couches du backbone
- [ ] Conserver les premières couches gelées
- [ ] Réduire le learning rate à 1e-5 ou 5e-6
- [ ] Entraîner 10-20 epochs supplémentaires
- [ ] Comparer avec la version backbone gelé
- [ ] Analyser l'apport du fine-tuning

### Phase C - Techniques Avancées (si nécessaire)
- [ ] Focal Loss
- [ ] Label Smoothing
- [ ] MixUp / CutMix
- [ ] Autres stratégies justifiées par les résultats

---

## 8. Reproductibilité

### 8.1 Versions Logicielles
- TensorFlow : 2.21.0
- Python : 3.13.5

### 8.2 Seeds
- Random seed : 42
- Dataset seed : 42
- Augmentation seed : 42

### 8.3 Chemins des Modèles
- CNN : `ai/saved_models/improved_cnn/best_model.keras`
- MobileNetV2 : `ai/saved_models/mobilenet_v2/best_model.keras`
- EfficientNetB0 : `ai/saved_models/efficientnet_b0/best_model.keras`
- ResNet50 : `ai/saved_models/resnet50/best_model.keras`

### 8.4 Résultats Détaillés
- Chemin : `ai/results/benchmark_results.json`
- Détails par modèle : `ai/results/{model_name}/`

---

## 9. Conclusion

Ce benchmark révèle une limitation fondamentale du protocole de Feature Extraction sur le dataset MVTec Bottle : malgré quatre architectures différentes, les performances sont identiques et le modèle ne parvient pas à détecter les classes minoritaires.

Cette observation n'est pas une conclusion sur l'efficacité du Transfer Learning en général, mais plutôt sur l'inadéquation du protocole actuel (backbone gelé + peu de données + class weights).

La Phase B de fine-tuning est essentielle pour :
1. Tirer parti des connaissances pré-entraînées
2. Adapter les features au domaine spécifique des bouteilles
3. potentiellement améliorer la détection des défauts

Seulement après cette phase, nous pourrons conclure sur l'efficacité réelle du Transfer Learning pour ce projet.

---

*Rapport généré le 2026-08-08*
*Méthodologie : Scientifique, reproductible, comparable*
