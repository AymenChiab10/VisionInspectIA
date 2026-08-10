"""
Chargement et inference du modele MobileNetV2 entraine.

Le modele est charge une seule fois (singleton), au demarrage de
l'application (voir app/main.py), et n'est jamais recharge par la suite.
"""

import sys
from pathlib import Path

import numpy as np
import tensorflow as tf

# backend/app/ml/model_loader.py -> remonte jusqu'a la racine du projet.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Rend le package "ai" (racine du projet, a cote de "backend") importable,
# quel que soit le repertoire courant depuis lequel le backend est lance.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Necessaire pour que Keras puisse reconstruire la couche de preprocessing
# personnalisee integree au modele sauvegarde (x / 127.5 - 1.0), voir
# ai/models/preprocessing_layers.py. Le backend ne depend ainsi que de la
# definition de cette couche, pas du reste du pipeline d'entrainement.
from ai.models.preprocessing_layers import MobileNetPreprocess  # noqa: F401,E402

from app.ml.labels import CLASS_NAMES  # noqa: E402

MODEL_PATH = PROJECT_ROOT / "ai" / "saved_models" / "mobilenet_v2" / "best_model.keras"


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
