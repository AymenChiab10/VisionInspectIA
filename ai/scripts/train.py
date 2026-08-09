"""
============================================================
Project : VisionInspectAI
File    : train.py
Author  : Aymen Chiab

Description:
    Train a CNN model using the prepared TensorFlow datasets.
============================================================
"""

from __future__ import annotations

import logging
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from ai.scripts.create_tf_dataset import DatasetLoader
from ai.models.model_factory import ModelFactory
from ai.training.trainer import Trainer
from ai.config.config import settings


class TrainPipeline:
    """
    Complete training pipeline.
    """

    def __init__(self) -> None:

        self.logger = self.setup_logger()

        self.dataset_loader = None

        self.model = None

        self.trainer = None

    # =====================================================
    # LOGGER
    # =====================================================

    def setup_logger(self) -> logging.Logger:
        """
        Configure pipeline logger.
        """

        logger = logging.getLogger("TrainPipeline")

        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        return logger

    # =====================================================
    # HEADER
    # =====================================================

    def print_header(self) -> None:
        """
        Print pipeline header.
        """

        print()

        print("=" * 60)

        print("VisionInspectAI")

        print("CNN Training")

        print("=" * 60)

        print()

    # =====================================================
    # LOAD DATASETS
    # =====================================================

    def load_datasets(self):
        """
        Load TensorFlow datasets.
        """

        self.logger.info("Loading TensorFlow datasets...")

        self.dataset_loader = DatasetLoader()

        self.dataset_loader.run()

        return (
            self.dataset_loader.train_dataset,
            self.dataset_loader.validation_dataset,
            self.dataset_loader.test_dataset,
        )

    # =====================================================
    # CREATE MODEL
    # =====================================================

    def create_model(self):
        """
        Create model using ModelFactory.
        """

        self.logger.info(
            f"Creating model: {settings.MODEL_TYPE}..."
        )

        self.model = ModelFactory.create_model(
            fine_tune=settings.FINE_TUNE
        )

        print()

        print("=" * 60)

        print("Model Architecture")

        print("=" * 60)

        print()

        self.model.summary()

        print()

        print(f"Total Parameters : {self.model.count_params():,}")

        print()

        return self.model

    # =====================================================
    # TRAIN
    # =====================================================

    def train(self) -> None:
        """
        Train the model.
        """

        train_dataset, validation_dataset, test_dataset = (
            self.load_datasets()
        )

        model = self.create_model()

        self.trainer = Trainer(
            model=model,
            train_dataset=train_dataset,
            validation_dataset=validation_dataset,
            test_dataset=test_dataset,
        )

        self.trainer.run()

    # =====================================================
    # RUN
    # =====================================================

    def run(self) -> None:
        """
        Execute complete training pipeline.
        """

        self.print_header()

        self.logger.info("Starting training pipeline...")

        try:

            self.train()

            self.logger.info("Training pipeline completed.")

        except Exception as error:

            self.logger.exception(f"Training failed: {error}")

            raise


# =====================================================
# MAIN
# =====================================================

def main() -> None:
    pipeline = TrainPipeline()

    pipeline.run()


if __name__ == "__main__":
    main()
