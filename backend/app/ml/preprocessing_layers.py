"""
Couche de preprocessing personnalisee integree au modele MobileNetV2 sauvegarde.

Copie exacte, non modifiee, de la classe MobileNetPreprocess definie dans
ai/models/preprocessing_layers.py (source d'entrainement). Dupliquee ici pour
que le backend soit autonome (deployable depuis le seul dossier backend/,
sans dependre du dossier ai/ comme repertoire frere) — necessaire car Keras
doit pouvoir reconstruire cette couche personnalisee au chargement du modele.
Aucune modification de logique : meme calcul, memes poids, meme comportement.
"""

from __future__ import annotations

import tensorflow as tf
import keras


@keras.saving.register_keras_serializable()
class MobileNetPreprocess(tf.keras.layers.Layer):
    """
    Preprocessing layer for MobileNetV2.

    Applies the official MobileNetV2 preprocessing:
        x = x / 127.5 - 1.0

    This is equivalent to:
        tf.keras.applications.mobilenet_v2.preprocess_input(x)

    Input range  : float32 [0, 255]
    Output range : float32 [-1, 1]
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, inputs):
        return tf.keras.applications.mobilenet_v2.preprocess_input(inputs)

    def get_config(self):
        config = super().get_config()
        return config
