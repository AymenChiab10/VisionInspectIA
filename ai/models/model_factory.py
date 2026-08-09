"""
============================================================
Project : VisionInspectAI
File    : model_factory.py
Author  : Aymen Chiab

Description:
    Factory for creating models based on configuration.
============================================================
"""

from __future__ import annotations

import tensorflow as tf

from ai.config.config import settings


class ModelFactory:
    """
    Create models based on configuration.
    """

    @staticmethod
    def create_model(fine_tune: bool = False) -> tf.keras.Model:
        """
        Create model based on settings.MODEL_TYPE.

        Args:
            fine_tune: If True, enable fine-tuning mode
                        for supported models.

        Returns:
            Compiled Keras model.
        """

        model_type = settings.MODEL_TYPE.lower()

        if model_type == "efficientnet":
            from ai.models.efficientnet_model import EfficientNetModel
            builder = EfficientNetModel()

        elif model_type == "mobilenet":
            from ai.models.mobilenet_model import MobileNetModel
            builder = MobileNetModel()

        elif model_type == "resnet":
            from ai.models.resnet_model import ResNetModel
            builder = ResNetModel()

        elif model_type == "cnn":
            from ai.models.cnn_model import CNNModel
            builder = CNNModel()

        else:
            raise ValueError(
                f"Unknown model type: {model_type}. "
                f"Choose from: efficientnet, mobilenet, resnet, cnn"
            )

        return builder.get_model(fine_tune=fine_tune)

    @staticmethod
    def get_available_models() -> list[str]:
        """
        Return list of available model types.

        Returns:
            List of model type names.
        """

        return ["efficientnet", "mobilenet", "resnet", "cnn"]
