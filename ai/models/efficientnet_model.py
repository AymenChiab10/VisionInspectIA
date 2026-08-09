"""
============================================================
Project : VisionInspectAI
File    : efficientnet_model.py
Author  : Aymen Chiab

Description:
    EfficientNetB0 transfer learning model for industrial
    defect classification.

Architecture:
    EfficientNetB0 (pretrained on ImageNet)
    GlobalAveragePooling2D
    Dropout
    Dense(4, softmax)
============================================================
"""

from __future__ import annotations

import tensorflow as tf

from ai.config.config import settings
from ai.training.metrics import get_classification_metrics


class EfficientNetModel:
    """
    EfficientNetB0 transfer learning model.
    """

    def __init__(self) -> None:

        self.input_shape = (
            settings.IMAGE_HEIGHT,
            settings.IMAGE_WIDTH,
            settings.IMAGE_CHANNELS,
        )

        self.num_classes = settings.NUM_CLASSES

        self.model = None

        self.base_model = None

    # =====================================================
    # BUILD MODEL
    # =====================================================

    def build(self, fine_tune: bool = False) -> tf.keras.Model:
        """
        Build EfficientNetB0 model.

        Args:
            fine_tune: If True, unfreeze the last 20 layers
                       for fine-tuning.

        Returns:
            Compiled Keras model.
        """

        inputs = tf.keras.Input(
            shape=self.input_shape,
            name="input"
        )

        x = inputs

        base_model = tf.keras.applications.EfficientNetB0(
            include_top=False,
            weights="imagenet",
            input_shape=self.input_shape,
            pooling=None,
        )

        if not fine_tune:
            base_model.trainable = False

        else:
            base_model.trainable = True

            for layer in base_model.layers[:-20]:
                layer.trainable = False

        x = base_model(x, training=not fine_tune)

        x = tf.keras.layers.GlobalAveragePooling2D(
            name="global_average_pooling"
        )(x)

        x = tf.keras.layers.Dropout(
            settings.DROPOUT_RATE,
            name="dropout"
        )(x)

        outputs = tf.keras.layers.Dense(
            self.num_classes,
            activation="softmax",
            kernel_regularizer=tf.keras.regularizers.l2(
                settings.WEIGHT_DECAY
            ),
            name="predictions"
        )(x)

        self.model = tf.keras.Model(
            inputs=inputs,
            outputs=outputs,
            name="EfficientNetB0"
        )

        self.base_model = base_model

        return self.model

    # =====================================================
    # COMPILE MODEL
    # =====================================================

    def compile_model(self) -> tf.keras.Model:
        """
        Compile the model.

        Returns:
            Compiled Keras model.
        """

        if self.model is None:
            self.build()

        optimizer = tf.keras.optimizers.Adam(
            learning_rate=settings.LEARNING_RATE
        )

        loss = tf.keras.losses.SparseCategoricalCrossentropy()

        metrics = get_classification_metrics()

        self.model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics
        )

        return self.model

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self) -> None:
        """
        Print model summary.
        """

        if self.model is None:
            self.build()

        self.model.summary()

    # =====================================================
    # PARAMETERS
    # =====================================================

    def count_parameters(self) -> int:
        """
        Count trainable parameters.

        Returns:
            Number of trainable parameters.
        """

        if self.model is None:
            self.build()

        trainable = self.model.count_params()

        print()

        print("=" * 60)

        print("Trainable Parameters")

        print("=" * 60)

        print(f"{trainable:,}")

        print()

        return trainable

    # =====================================================
    # GET MODEL
    # =====================================================

    def get_model(self, fine_tune: bool = False) -> tf.keras.Model:
        """
        Build and compile model.

        Args:
            fine_tune: If True, unfreeze last layers.

        Returns:
            Compiled Keras model.
        """

        if self.model is None:
            self.build(fine_tune=fine_tune)
            self.compile_model()

        return self.model
