"""
============================================================
Project : VisionInspectAI
File    : callbacks.py
Author  : Aymen Chiab

Description:
    TensorFlow callbacks used during model training.
============================================================
"""

from __future__ import annotations

from pathlib import Path

import tensorflow as tf

from ai.config.config import settings

class TrainingCallbacks:
    """
    Create TensorFlow callbacks.
    """

    def __init__(self):

        self.checkpoint_dir = (
            settings.CHECKPOINTS_PATH
        )

        self.logs_dir = (
            settings.LOGS_PATH
        )

        self.checkpoint_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.logs_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        # =====================================================
    # MODEL CHECKPOINT
    # =====================================================

    def create_checkpoint(self):

        return tf.keras.callbacks.ModelCheckpoint(

            filepath=str(

                self.checkpoint_dir /

                "best_model.keras"

            ),

            monitor=settings.CHECKPOINT_MONITOR,

            mode=settings.CHECKPOINT_MODE,

            save_best_only=settings.SAVE_BEST_ONLY,

            verbose=1

        )
        # =====================================================
    # EARLY STOPPING
    # =====================================================

    def create_early_stopping(self):

        return tf.keras.callbacks.EarlyStopping(

            monitor="val_loss",

            patience=settings.EARLY_STOPPING_PATIENCE,

            restore_best_weights=True,

            verbose=1

        )
        # =====================================================
    # REDUCE LR
    # =====================================================

    def create_reduce_lr(self):

        return tf.keras.callbacks.ReduceLROnPlateau(

            monitor="val_loss",

            factor=settings.REDUCE_LR_FACTOR,

            patience=settings.REDUCE_LR_PATIENCE,

            min_lr=settings.MIN_LEARNING_RATE,

            verbose=1

        )
        # =====================================================
    # CSV LOGGER
    # =====================================================

    def create_csv_logger(self):
        """
        Save training history to CSV.
        """

        return tf.keras.callbacks.CSVLogger(

            filename=str(
                settings.CSV_LOGGER_FILE
            ),

            separator=",",

            append=False

        )
        # =====================================================
    # TENSORBOARD
    # =====================================================

    def create_tensorboard(self):
        """
        TensorBoard callback.
        """

        return tf.keras.callbacks.TensorBoard(

            log_dir=str(
                settings.TENSORBOARD_LOG_DIR
            ),

            histogram_freq=1,

            write_graph=True,

            write_images=False,

            update_freq="epoch"

        )
        # =====================================================
    # GET CALLBACKS
    # =====================================================

    def get_callbacks(self):
        """
        Return all callbacks.
        """

        callbacks = [

            self.create_checkpoint(),

            self.create_early_stopping(),

            self.create_csv_logger(),

            self.create_tensorboard()

        ]

        return callbacks
# =====================================================
# MAIN
# =====================================================

def main():

    callbacks = TrainingCallbacks().get_callbacks()

    print()

    print("=" * 60)

    print("TensorFlow Callbacks")

    print("=" * 60)

    for callback in callbacks:

        print(callback.__class__.__name__)


if __name__ == "__main__":

    main()        