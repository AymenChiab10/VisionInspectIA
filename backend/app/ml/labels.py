"""
Liste des classes de prediction, dans le meme ordre que celui utilise a
l'entrainement (voir ai/config/config.py, CLASSES).

Cet ordre correspond directement aux indices de sortie du modele
MobileNetV2 (couche "predictions", softmax a 4 sorties). Ne jamais
modifier cet ordre : cela decalerait les classes predites.
"""

CLASS_NAMES = [
    "broken_large",
    "broken_small",
    "contamination",
    "good",
]
