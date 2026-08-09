"""
============================================================
Project : VisionInspectAI
File    : verify_experiments.py
Author  : Aymen Chiab

Description:
    Verify that the 3 experiment modes load correctly.

    For each mode, this script prints:
      - experiment name
      - dataset type
      - train / validation / test paths
      - augmentation state
      - number of batches
      - class names

    No model training is performed.
============================================================
"""

from __future__ import annotations

import logging
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import tensorflow as tf

from ai.config.config import Settings
from ai.scripts.create_tf_dataset import DatasetLoader


def verify_mode(mode: str) -> None:
    """
    Verify one experiment mode.
    """

    print()
    print("=" * 60)
    print(f"Experiment mode : {mode}")
    print("=" * 60)

    original_mode = Settings.EXPERIMENT_MODE
    Settings.EXPERIMENT_MODE = mode

    try:
        loader = DatasetLoader()

        print(f"Name            : {loader.experiment_name}")
        print(f"Dataset type    : {loader.dataset_type}")
        print(f"Augmentation    : {loader.augmentation_enabled}")
        print(f"Train path      : {loader.train_path}")
        print(f"Validation path : {loader.validation_path}")
        print(f"Test path       : {loader.test_path}")

        loader.create_datasets()

        train_batches = int(
            tf.data.experimental.cardinality(loader.train_dataset).numpy()
        )
        val_batches = int(
            tf.data.experimental.cardinality(loader.validation_dataset).numpy()
        )
        test_batches = int(
            tf.data.experimental.cardinality(loader.test_dataset).numpy()
        )

        print(f"Train batches   : {train_batches}")
        print(f"Val batches     : {val_batches}")
        print(f"Test batches    : {test_batches}")

        if loader.class_names:
            print(f"Classes         : {loader.class_names}")

        images, labels = next(iter(loader.train_dataset))
        print(f"Train batch shape: {images.shape}")
        print(f"Labels shape     : {labels.shape}")

    finally:
        Settings.EXPERIMENT_MODE = original_mode


def main() -> None:
    """
    Verify all experiment modes.
    """

    modes = ["raw_no_aug", "raw_onfly", "augmented_offline"]

    for mode in modes:
        verify_mode(mode)


if __name__ == "__main__":
    main()
