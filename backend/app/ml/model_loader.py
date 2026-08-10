"""
Chargement et inference du modele MobileNetV2 entraine.

Le modele est charge une seule fois (singleton), au demarrage de
l'application (voir app/main.py), et n'est jamais recharge par la suite.
"""

from pathlib import Path

import numpy as np
import tensorflow as tf

# Necessaire pour que Keras puisse reconstruire la couche de preprocessing
# personnalisee integree au modele sauvegarde (x / 127.5 - 1.0). Copie exacte
# de ai/models/preprocessing_layers.py, dupliquee dans le backend pour que
# celui-ci soit deployable de maniere autonome (voir preprocessing_layers.py
# pour le detail de cette duplication).
from app.ml.preprocessing_layers import MobileNetPreprocess  # noqa: F401

from app.core.config import settings
from app.ml.labels import CLASS_NAMES

# Chemin par defaut : copie du modele final embarquee dans le backend
# (backend/app/ml/model_files/best_model.keras, poids identiques a
# ai/saved_models/mobilenet_v2/best_model.keras). Surchargeable via la
# variable d'environnement MODEL_PATH (ex: sur une plateforme cloud avec un
# volume monte ailleurs).
DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "model_files" / "best_model.keras"
MODEL_PATH = Path(settings.MODEL_PATH) if settings.MODEL_PATH else DEFAULT_MODEL_PATH


class ModelLoader:
    """Encapsule le modele Keras charge et expose une methode predict()."""

    def __init__(self) -> None:
        self._model: tf.keras.Model | None = None

    def load_model(self) -> None:
        """Charge le modele .keras en memoire. A appeler une seule fois."""
        if self._model is None:
            self._model = tf.keras.models.load_model(MODEL_PATH)

    def predict(self, image: tf.Tensor) -> tuple[str, float]:
        """
        Effectue une inference sur une image deja pretraitee.

        Retourne un tuple (classe_predite, score_de_confiance).
        """
        if self._model is None:
            raise RuntimeError(
                "Le modele MobileNetV2 n'est pas charge. "
                "Appeler load_model() au demarrage de l'application."
            )

        predictions = self._model.predict(image, verbose=0)
        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_index])

        return CLASS_NAMES[predicted_index], confidence


# Instance unique, partagee par toute l'application (singleton).
model_loader = ModelLoader()
