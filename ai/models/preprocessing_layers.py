"""
============================================================
Project : VisionInspectAI
File    : preprocessing_layers.py
Author  : Aymen Chiab

Description:
    Dedicated preprocessing layers for transfer learning
    architectures. Each layer encapsulates the official
    TensorFlow/Keras preprocessing function for its
    respective backbone.

    This approach ensures:
    - Explicit and readable preprocessing
    - Proper serialization/deserialization
    - Clean model export
    - Separation of concerns
============================================================
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


@keras.saving.register_keras_serializable()
class EfficientNetPreprocess(tf.keras.layers.Layer):
    """
    Preprocessing layer for EfficientNetB0.

    This layer is a NO-OP placeholder.

    In TensorFlow >= 2.11, EfficientNetB0 integrates its own
    preprocessing directly into the model architecture:
        - Rescaling(1/255)
        - Normalization(mean=[0.485, 0.456, 0.406],
                        variance=[0.229, 0.224, 0.225])
        - Rescaling(per-channel scale)

    The official preprocess_input function is deprecated and
    does nothing. Adding external preprocessing would result
    in double-processing and corrupt the input distribution.

    This layer exists for API consistency and explicitness,
    but performs no operation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, inputs):
        return inputs

    def get_config(self):
        config = super().get_config()
        return config


@keras.saving.register_keras_serializable()
class ResNetPreprocess(tf.keras.layers.Layer):
    """
    Preprocessing layer for ResNet50.

    Applies the official ResNet50 preprocessing:
        - RGB to BGR conversion
        - Subtraction of ImageNet channel means

    This is equivalent to:
        tf.keras.applications.resnet50.preprocess_input(x)

    Input range  : float32 [0, 255] (RGB)
    Output range : float32 BGR with centered values
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, inputs):
        return tf.keras.applications.resnet50.preprocess_input(inputs)

    def get_config(self):
        config = super().get_config()
        return config
