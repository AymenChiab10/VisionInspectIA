"""
Preprocessing de l'image envoyee au modele MobileNetV2.

Reproduit exactement le pipeline utilise a l'entrainement par
ai/scripts/create_tf_dataset.py (via tf.keras.utils.image_dataset_from_directory) :
- decodage en RGB (3 canaux) ;
- redimensionnement bilineaire en 224x224 ;
- conversion en float32, valeurs dans la plage [0, 255].

Important : la normalisation MobileNetV2 (x / 127.5 - 1.0) n'est PAS
appliquee ici. Elle est deja integree dans le graphe du modele sauvegarde
(couche "preprocess", voir ai/models/preprocessing_layers.py). L'appliquer
une seconde fois corromprait les predictions.
"""

import tensorflow as tf

# Doit rester strictement identique a IMAGE_SIZE dans ai/config/config.py.
IMAGE_SIZE = (224, 224)


def preprocess_image(image_bytes: bytes) -> tf.Tensor:
    """
    Transforme les octets bruts d'une image uploadee en tenseur pret pour
    le modele.

    Retourne un tenseur de forme (1, 224, 224, 3), dtype float32,
    valeurs dans [0, 255].
    """
    image = tf.io.decode_image(image_bytes, channels=3, expand_animations=False)
    image = tf.image.resize(image, IMAGE_SIZE, method="bilinear")
    image = tf.cast(image, tf.float32)
    image = tf.expand_dims(image, axis=0)
    return image
