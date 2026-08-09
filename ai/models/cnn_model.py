"""
============================================================
Project : VisionInspectAI
File    : cnn_model.py
Author  : Aymen Chiab

Description:
    Improved custom CNN model for industrial defect
    classification with modern architecture.

Architecture:
    Conv2D + BN + ReLU
    Conv2D + BN + ReLU
    MaxPooling
    SE Block
    Repeat x6 blocks
    GlobalAveragePooling
    Dense + BN + ReLU + Dropout
    Dense(4, softmax)
============================================================
"""

from __future__ import annotations

import tensorflow as tf

from ai.config.config import settings
from ai.training.metrics import get_classification_metrics


class CNNModel:
    """
    Improved custom CNN architecture with modern techniques.
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
    # CONVOLUTION BLOCK
    # =====================================================

    @staticmethod
    def convolution_block(
        x,
        filters: int,
        block_name: str,
        kernel_size: int = 3,
        stride: int = 1,
        use_se: bool = False,
    ):
        """
        Convolution block with optional SE block.

        Conv2D + BN + ReLU + MaxPooling + SE
        """

        x = tf.keras.layers.Conv2D(
            filters,
            kernel_size=kernel_size,
            strides=stride,
            padding="same",
            use_bias=False,
            kernel_regularizer=tf.keras.regularizers.l2(
                settings.WEIGHT_DECAY
            ),
            name=f"conv_{block_name}_{filters}",
        )(x)

        x = tf.keras.layers.BatchNormalization(
            name=f"bn_{block_name}_{filters}"
        )(x)

        x = tf.keras.layers.ReLU(
            name=f"relu_{block_name}_{filters}"
        )(x)

        x = tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2),
            name=f"pool_{block_name}_{filters}",
        )(x)

        if use_se:
            x = CNNModel.se_block(x, filters, name=f"se_{block_name}_{filters}")

        return x

    # =====================================================
    # SE BLOCK (Squeeze-and-Excitation)
    # =====================================================

    @staticmethod
    def se_block(x, filters: int, name: str = "se"):
        """
        Squeeze-and-Excitation block for channel attention.
        """

        se = tf.keras.layers.GlobalAveragePooling2D(
            name=f"{name}_gap"
        )(x)

        se = tf.keras.layers.Dense(
            filters // 4,
            use_bias=False,
            kernel_regularizer=tf.keras.regularizers.l2(
                settings.WEIGHT_DECAY
            ),
            name=f"{name}_dense1",
        )(se)

        se = tf.keras.layers.ReLU(
            name=f"{name}_relu"
        )(se)

        se = tf.keras.layers.Dense(
            filters,
            use_bias=False,
            kernel_regularizer=tf.keras.regularizers.l2(
                settings.WEIGHT_DECAY
            ),
            name=f"{name}_dense2",
        )(se)

        se = tf.keras.layers.Activation(
            "sigmoid",
            name=f"{name}_sigmoid"
        )(se)

        se = tf.keras.layers.Reshape(
            (1, 1, filters),
            name=f"{name}_reshape"
        )(se)

        x = tf.keras.layers.Multiply(
            name=f"{name}_multiply"
        )([x, se])

        return x

    # =====================================================
    # CLASSIFICATION HEAD
    # =====================================================

    @staticmethod
    def classification_head(x):
        """
        Classification head with dropout and dense layers.
        """

        x = tf.keras.layers.GlobalAveragePooling2D(
            name="global_average_pooling"
        )(x)

        x = tf.keras.layers.Dropout(
            settings.DROPOUT_RATE,
            name="dropout_1"
        )(x)

        x = tf.keras.layers.Dense(
            256,
            use_bias=False,
            kernel_regularizer=tf.keras.regularizers.l2(
                settings.WEIGHT_DECAY
            ),
            name="dense_256",
        )(x)

        x = tf.keras.layers.BatchNormalization(
            name="bn_dense"
        )(x)

        x = tf.keras.layers.ReLU(
            name="relu_dense"
        )(x)

        x = tf.keras.layers.Dropout(
            settings.DROPOUT_RATE,
            name="dropout_2"
        )(x)

        return x

    # =====================================================
    # BUILD MODEL
    # =====================================================

    def build(self) -> tf.keras.Model:
        """
        Build improved CNN architecture.
        """

        inputs = tf.keras.Input(
            shape=self.input_shape,
            name="input"
        )

        x = inputs

        x = tf.keras.layers.Rescaling(
            scale=1.0 / 255.0,
            name="preprocess"
        )(x)

        # -------------------------------------------------
        # Block 1: 224 -> 112
        # -------------------------------------------------
        x = self.convolution_block(
            x,
            filters=32,
            block_name="block1",
            use_se=False,
        )

        # -------------------------------------------------
        # Block 2: 112 -> 56
        # -------------------------------------------------
        x = self.convolution_block(
            x,
            filters=64,
            block_name="block2",
            use_se=True,
        )

        # -------------------------------------------------
        # Block 3: 56 -> 28
        # -------------------------------------------------
        x = self.convolution_block(
            x,
            filters=128,
            block_name="block3",
            use_se=True,
        )

        # -------------------------------------------------
        # Block 4: 28 -> 14
        # -------------------------------------------------
        x = self.convolution_block(
            x,
            filters=256,
            block_name="block4",
            use_se=True,
        )

        # -------------------------------------------------
        # Block 5: 14 -> 7
        # -------------------------------------------------
        x = self.convolution_block(
            x,
            filters=512,
            block_name="block5",
            use_se=True,
        )

        # -------------------------------------------------
        # Classification Head
        # -------------------------------------------------
        x = self.classification_head(x)

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
            name="VisionInspectCNN"
        )

        return self.model

    # =====================================================
    # COMPILE MODEL
    # =====================================================

    def compile_model(self) -> tf.keras.Model:
        """
        Compile the model with AdamW and cosine decay.
        """

        if self.model is None:
            self.build()

        steps_per_epoch = settings.TRAIN_STEPS_PER_EPOCH

        lr_schedule = tf.keras.optimizers.schedules.CosineDecay(
            initial_learning_rate=settings.LEARNING_RATE,
            decay_steps=steps_per_epoch * settings.EPOCHS,
            alpha=settings.MIN_LEARNING_RATE / settings.LEARNING_RATE,
        )

        optimizer = tf.keras.optimizers.AdamW(
            learning_rate=lr_schedule,
            weight_decay=settings.WEIGHT_DECAY,
            global_clipnorm=1.0,
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
    # SAVE MODEL DIAGRAM
    # =====================================================

    def plot_model(self) -> None:
        """
        Save model architecture diagram.
        """

        if self.model is None:
            self.build()

        tf.keras.utils.plot_model(
            self.model,
            to_file=str(
                settings.FIGURES_PATH /
                "cnn_architecture.png"
            ),
            show_shapes=True,
            show_dtype=True,
            expand_nested=True,
        )

    # =====================================================
    # GET MODEL
    # =====================================================

    def get_model(self, fine_tune: bool = False) -> tf.keras.Model:
        """
        Build and compile model.

        Args:
            fine_tune: Ignored for CNN. Kept for API compatibility.

        Returns:
            Compiled Keras model.
        """

        if self.model is None:
            self.build()
            self.compile_model()

        return self.model
