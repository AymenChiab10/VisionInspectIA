"""
============================================================
Project : VisionInspectAI
File    : visualize_dataset.py
Author  : Aymen Chiab

Description:
    Visual dataset inspection for the MVTec Bottle dataset.

    Displays original images, offline augmented images,
    and on-the-fly augmented examples for each class.

    This step is performed before any new training experiment
    to verify that:
      - defects remain visible after augmentation;
      - transformations are realistic;
      - no obvious artifacts are created.

    No model training is performed in this script.
============================================================
"""

from __future__ import annotations

import json
import logging
import sys
import random
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from ai.config.config import settings
from ai.scripts.data_augmentation import ImageAugmenter


class DatasetVisualizer:
    """
    Visual dataset inspector.

    Generates comparison grids for each class:
      original, offline augmented, on-the-fly augmented.
    """

    def __init__(
        self,
        num_samples: int = 5,
        figsize: tuple[int, int] = (15, 5),
        dpi: int = 150,
    ) -> None:

        self.num_samples = num_samples

        self.figsize = figsize

        self.dpi = dpi

        self.output_dir = settings.FIGURES_PATH

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.logger = self.setup_logger()

        self.logger.info("DatasetVisualizer initialized.")

    # =====================================================
    # LOGGER
    # =====================================================

    def setup_logger(self) -> logging.Logger:
        """
        Configure logger.
        """

        logger = logging.getLogger("DatasetVisualizer")

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
    # IMAGE LOADING
    # =====================================================

    def load_image(self, path: Path) -> np.ndarray:
        """
        Load an image as a uint8 numpy array.
        """

        image = tf.keras.utils.load_img(path, target_size=settings.IMAGE_SIZE)

        image_array = tf.keras.utils.img_to_array(image)

        return np.clip(image_array, 0, 255).astype(np.uint8)

    def collect_images(self, folder: Path, max_samples: int) -> list[Path]:
        """
        Collect image paths from a folder.
        """

        extensions = ["*.png", "*.jpg", "*.jpeg"]

        images: list[Path] = []

        for ext in extensions:
            images.extend(folder.glob(ext))

        images = sorted(images)[:max_samples]

        return images

    # =====================================================
    # OFFLINE AUGMENTATION EXAMPLES
    # =====================================================

    def get_offline_augmented_paths(
        self,
        original_paths: list[Path],
    ) -> list[Path]:
        """
        Find corresponding augmented images for a list of originals.

        The augmented dataset follows the naming pattern:
          <stem>_aug_<idx>.png
        """

        augmented_paths: list[Path] = []

        for path in original_paths:
            stem = path.stem

            parent = path.parent

            candidates = sorted(parent.glob(f"{stem}_aug_*.png"))

            if candidates:
                augmented_paths.append(candidates[0])
            else:
                augmented_paths.append(path)

        return augmented_paths

    # =====================================================
    # ON-THE-FLY AUGMENTATION EXAMPLES
    # =====================================================

    def apply_on_the_fly_augmentation(
        self,
        images: np.ndarray,
    ) -> np.ndarray:
        """
        Apply the on-the-fly augmentation pipeline to a batch.
        """

        augmenter = ImageAugmenter()

        augmenter.pipeline = augmenter.build_pipeline()

        image_tensors = tf.convert_to_tensor(images, dtype=tf.float32)

        augmented = augmenter.pipeline(image_tensors, training=True)

        augmented_np = augmented.numpy()

        return np.clip(augmented_np, 0, 255).astype(np.uint8)

    # =====================================================
    # PLOTTING
    # =====================================================

    def plot_class_grid(
        self,
        class_name: str,
        originals: list[np.ndarray],
        offline: list[np.ndarray],
        onthefly: list[np.ndarray],
    ) -> None:
        """
        Plot a comparison grid for one class.
        """

        num_samples = len(originals)

        fig, axes = plt.subplots(
            nrows=3,
            ncols=num_samples,
            figsize=self.figsize,
            dpi=self.dpi,
        )

        fig.suptitle(
            f"Class: {class_name}\n"
            f"Original | Offline Augmented | On-the-fly Augmented",
            fontsize=14,
        )

        for idx in range(num_samples):
            axes[0, idx].imshow(originals[idx])

            axes[0, idx].axis("off")

            axes[0, idx].set_title("Original")

            axes[1, idx].imshow(offline[idx])

            axes[1, idx].axis("off")

            axes[1, idx].set_title("Offline")

            axes[2, idx].imshow(onthefly[idx])

            axes[2, idx].axis("off")

            axes[2, idx].set_title("On-the-fly")

        plt.tight_layout()

        output_path = self.output_dir / f"visual_inspection_{class_name}.png"

        plt.savefig(output_path, dpi=self.dpi, bbox_inches="tight")

        plt.close()

        self.logger.info(f"Saved visual inspection: {output_path}")

    # =====================================================
    # CLASS INSPECTION
    # =====================================================

    def inspect_class(
        self,
        class_name: str,
        original_dir: Path,
        augmented_dir: Path,
    ) -> None:
        """
        Inspect one class: original, offline augmented, on-the-fly augmented.
        """

        self.logger.info(f"Inspecting class: {class_name}")

        original_paths = self.collect_images(
            original_dir,
            self.num_samples,
        )

        if not original_paths:
            self.logger.warning(f"No images found for {class_name}")

            return

        originals = [self.load_image(path) for path in original_paths]

        offline_paths = self.get_offline_augmented_paths(original_paths)

        offline_images = [self.load_image(path) for path in offline_paths]

        onthefly_images = self.apply_on_the_fly_augmentation(
            np.array(originals)
        )

        self.plot_class_grid(
            class_name=class_name,
            originals=originals,
            offline=offline_images,
            onthefly=list(onthefly_images),
        )

    # =====================================================
    # GLOBAL INSPECTION
    # =====================================================

    def run(self) -> None:
        """
        Run visual inspection for all classes.
        """

        self.logger.info("Starting visual inspection...")

        classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination",
        ]

        original_base = settings.PROCESSED_DATA_PATH / "bottle" / "train"

        augmented_base = settings.AUGMENTED_BOTTLE_PATH / "train"

        for class_name in classes:
            original_dir = original_base / class_name

            augmented_dir = augmented_base / class_name

            self.inspect_class(
                class_name=class_name,
                original_dir=original_dir,
                augmented_dir=augmented_dir,
            )

        self.logger.info("Visual inspection completed.")

        self.export_summary()

    # =====================================================
    # SUMMARY
    # =====================================================

    def export_summary(self) -> None:
        """
        Export a JSON summary of the visual inspection.
        """

        summary = {
            "num_samples_per_class": self.num_samples,
            "classes": [
                "good",
                "broken_large",
                "broken_small",
                "contamination",
            ],
            "output_dir": str(self.output_dir),
            "figures": [
                str(self.output_dir / f"visual_inspection_{cls}.png")
                for cls in [
                    "good",
                    "broken_large",
                    "broken_small",
                    "contamination",
                ]
            ],
        }

        output_path = self.output_dir / "visual_inspection_summary.json"

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(summary, file, indent=4)

        self.logger.info(f"Summary saved: {output_path}")


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    """
    Run visual inspection.
    """

    visualizer = DatasetVisualizer(
        num_samples=5,
        figsize=(15, 5),
        dpi=150,
    )

    visualizer.run()


if __name__ == "__main__":
    main()
