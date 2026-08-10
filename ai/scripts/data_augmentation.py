"""
============================================================
Project : VisionInspectAI
File    : data_augmentation.py
Author  : Aymen Chiab

Description:
    Data augmentation and dataset balancing for the
    MVTec Bottle dataset.
============================================================
"""

from __future__ import annotations

import json
import logging
import random
import shutil
import sys

from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import tensorflow as tf

import numpy as np

from tqdm import tqdm

from ai.config.config import settings

from ai.utils.file_utils import (
    ensure_directory,
    get_image_files,
)

from ai.utils.image_utils import (
    copy_image,
    load_image,
    save_image,
)


class ImageAugmenter:
    """
    Data augmentation and dataset balancing.
    """

    def __init__(self):
        random.seed(settings.AUGMENTATION_SEED)

        tf.random.set_seed(
            settings.AUGMENTATION_SEED
        )

        self.input_dataset = (
            settings.PROCESSED_DATA_PATH /
            "bottle"
        )

        self.output_dataset = (
            settings.AUGMENTED_BOTTLE_PATH
        )

        self.train_target = (
            settings.TRAIN_IMAGES_PER_CLASS
        )

        self.validation_target = (
            settings.VALIDATION_IMAGES_PER_CLASS
        )

        self.test_target = (
            settings.TEST_IMAGES_PER_CLASS
        )

        self.pipeline = None

        self.report = {}

        self.logger = self.setup_logger()

        self.logger.info(
            "ImageAugmenter initialized."
        )

    # =====================================================
    # LOGGER
    # =====================================================

    def setup_logger(self):
        """
        Configure project logger.
        """

        logger = logging.getLogger("ImageAugmenter")

        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        settings.LOGS_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

        file_handler = logging.FileHandler(
            settings.LOGS_PATH / "augmentation.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    # =====================================================
    # HEADER
    # =====================================================

    def print_header(self):
        """
        Display header.
        """

        print()

        print("=" * 60)

        print("VisionInspectAI")

        print("Data Augmentation")

        print("=" * 60)

        print()

        print(f"Input  : {self.input_dataset}")

        print(f"Output : {self.output_dataset}")

        print()

    # =====================================================
    # VALIDATE DATASET
    # =====================================================

    def validate_dataset(self):
        """
        Validate processed dataset.
        """

        self.logger.info(
            "Checking processed dataset..."
        )

        if not self.input_dataset.exists():

            raise FileNotFoundError(
                f"{self.input_dataset} not found."
            )

        required_splits = [
            "train",
            "validation",
            "test"
        ]

        required_classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination"
        ]

        for split in required_splits:

            split_path = self.input_dataset / split

            if not split_path.exists():

                raise FileNotFoundError(
                    f"{split_path} not found."
                )

            for cls in required_classes:

                folder = split_path / cls

                if not folder.exists():

                    raise FileNotFoundError(
                        f"{folder} not found."
                    )

                images = get_image_files(folder)

                if len(images) == 0:

                    raise ValueError(
                        f"No images inside {folder}"
                    )

        self.logger.info(
            "Dataset validated."
        )

    # =====================================================
    # INITIALIZE REPORT
    # =====================================================

    def initialize_report(self):
        """
        Initialize augmentation report.
        """

        self.report = {
            "generated_at": str(
                datetime.now()
            ),
            "train": {},
            "validation": {},
            "test": {}
        }

    # =====================================================
    # CREATE OUTPUT STRUCTURE
    # =====================================================

    def create_output_structure(self):
        """
        Create output folders.
        """

        self.logger.info(
            "Creating folders..."
        )

        if self.output_dataset.exists():

            shutil.rmtree(
                self.output_dataset
            )

        splits = [
            "train",
            "validation",
            "test"
        ]

        classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination"
        ]

        for split in splits:

            for cls in classes:

                ensure_directory(
                    self.output_dataset /
                    split /
                    cls
                )

        self.logger.info(
            "Folders created."
        )

    # =====================================================
    # BUILD AUGMENTATION PIPELINE
    # =====================================================

    def build_pipeline(self):
        """
        Build TensorFlow augmentation pipeline.

        Experimentation "Priorite 1" (amelioration de la generalisation) :
        ajout de RandomBrightness, seule nouvelle variable introduite par
        rapport a la baseline. Cible directement l'absence de diversite
        photometrique du dataset MVTec (une seule seance de prise de vue,
        un seul eclairage) - la variation la plus frequente entre une
        photo de studio et une photo "reelle". Toutes les autres couches
        sont inchangees par rapport a la baseline pour isoler cette seule
        variable.
        """

        return tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip(
                    mode="horizontal",
                    seed=settings.AUGMENTATION_SEED
                ),
                tf.keras.layers.RandomRotation(
                    factor=0.05,
                    seed=settings.AUGMENTATION_SEED
                ),
                tf.keras.layers.RandomZoom(
                    height_factor=(-0.10, 0.10),
                    width_factor=(-0.10, 0.10),
                    seed=settings.AUGMENTATION_SEED
                ),
                tf.keras.layers.RandomTranslation(
                    height_factor=0.05,
                    width_factor=0.05,
                    seed=settings.AUGMENTATION_SEED
                ),
                tf.keras.layers.RandomContrast(
                    factor=0.10,
                    seed=settings.AUGMENTATION_SEED
                ),
                tf.keras.layers.RandomBrightness(
                    factor=0.15,
                    value_range=(0, 255),
                    seed=settings.AUGMENTATION_SEED
                )
            ],
            name="augmentation_pipeline"
        )

    # =====================================================
    # AUGMENT SINGLE IMAGE
    # =====================================================

    def augment_image(
        self,
        image_tensor
    ):
        """
        Apply augmentation pipeline to a single image tensor.
        """

        image_tensor = tf.expand_dims(
            image_tensor,
            axis=0
        )

        image_tensor = self.pipeline(
            image_tensor,
            training=True
        )

        return tf.squeeze(
            image_tensor,
            axis=0
        )

    # =====================================================
    # AUGMENT TRAIN
    # =====================================================

    def augment_train(self):
        """
        Augment all training classes.
        """

        classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination"
        ]

        for class_name in classes:

            self.augment_class(class_name)

    # =====================================================
    # AUGMENT CLASS
    # =====================================================

    def augment_class(
        self,
        class_name: str
    ):
        """
        Augment one training class until the target size.
        """

        self.logger.info(
            f"Augmenting {class_name}"
        )

        input_folder = (
            self.input_dataset /
            "train" /
            class_name
        )

        output_folder = (
            self.output_dataset /
            "train" /
            class_name
        )

        images = get_image_files(
            input_folder
        )

        current = len(images)

        target = self.train_target

        generated = max(0, target - current)

        print(
            f"{class_name} : "
            f"{current} -> "
            f"{target}"
        )

        for source_path in images:

            copy_image(
                source_path,
                output_folder / source_path.name
            )

        for idx in tqdm(
            range(generated),
            desc=f"Augmenting {class_name}",
            unit="image"
        ):

            source_path = images[idx % current]

            image = load_image(source_path)

            image_tensor = tf.convert_to_tensor(
                image,
                dtype=tf.float32
            )

            augmented_tensor = self.augment_image(
                image_tensor
            )

            augmented_image = np.clip(
                augmented_tensor.numpy(),
                0,
                255
            ).astype(np.uint8)

            output_path = (
                output_folder /
                f"{source_path.stem}_aug_{idx}.png"
            )

            save_image(augmented_image, output_path)

        self.logger.info(
            f"Augmented {class_name}: generated {generated} images."
        )

    # =====================================================
    # BALANCE VALIDATION
    # =====================================================

    def balance_validation(self):
        """
        Balance validation dataset.

        pad=False : contrairement au test, la validation n'est jamais
        completee par des copies dupliquees. Un signal de validation
        base sur des doublons est bruite et fausse les decisions
        d'early stopping / selection du meilleur checkpoint pendant
        l'entrainement. On garde donc uniquement les images reelles
        uniques disponibles, quitte a avoir moins que la cible.
        """

        self.balance_split(
            split_name="validation",
            target=self.validation_target,
            pad=False
        )

    # =====================================================
    # BALANCE SPLIT
    # =====================================================

    def balance_split(
        self,
        split_name: str,
        target: int,
        pad: bool = True
    ):
        """
        Balance a dataset split.

        pad=True  : complete jusqu'a target par des copies dupliquees
                    (comportement historique, utilise pour le test).
        pad=False : ne copie que les images reelles disponibles, sans
                    jamais dupliquer (utilise pour la validation).
        """

        self.logger.info(
            f"Balancing {split_name}..."
        )

        classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination"
        ]

        for class_name in classes:

            self.balance_class(
                split_name,
                class_name,
                target,
                pad=pad
            )

    # =====================================================
    # BALANCE CLASS
    # =====================================================

    def balance_class(
        self,
        split_name: str,
        class_name: str,
        target: int,
        pad: bool = True
    ):
        """
        Copie les images reelles disponibles. Si pad=True, duplique
        jusqu'a atteindre target ; si pad=False, ne duplique jamais
        (le split peut alors contenir moins d'images que target).
        """

        input_folder = (
            self.input_dataset /
            split_name /
            class_name
        )

        output_folder = (
            self.output_dataset /
            split_name /
            class_name
        )

        images = get_image_files(
            input_folder
        )

        current = len(images)

        print(
            f"{split_name} - "
            f"{class_name} : "
            f"{current} -> "
            f"{target if pad else current}"
        )

        if current > target:

            images = random.sample(images, target)

            current = target

        for idx in range(current):

            copy_image(
                images[idx],
                output_folder / images[idx].name
            )

        if not pad:
            self.logger.info(
                f"Balanced {split_name}/{class_name}: "
                f"{current} images reelles, aucune copie dupliquee."
            )
            return

        needed = max(0, target - current)

        for idx in range(needed):

            source = images[idx % current]

            destination = (
                output_folder /
                f"{source.stem}_copy_{idx}.png"
            )

            copy_image(source, destination)

        self.logger.info(
            f"Balanced {split_name}/{class_name}: {current} -> {target}"
        )

    # =====================================================
    # BALANCE TEST
    # =====================================================

    def balance_test(self):
        """
        Balance test dataset.
        """

        self.balance_split(
            split_name="test",
            target=self.test_target
        )

    # =====================================================
    # VERIFY DATASET
    # =====================================================

    def verify_dataset(self):
        """
        Verify the augmented dataset.
        """

        print()

        print("=" * 60)

        print("Dataset Verification")

        print("=" * 60)

        verification = {}

        splits = [
            "train",
            "validation",
            "test"
        ]

        classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination"
        ]

        for split in splits:

            verification[split] = {}

            print()

            print(split.upper())

            total = 0

            for class_name in classes:

                folder = (
                    self.output_dataset /
                    split /
                    class_name
                )

                count = len(
                    get_image_files(folder)
                )

                verification[split][class_name] = count

                total += count

                print(
                    f"{class_name:<20}"
                    f"{count}"
                )

            print(
                f"{'TOTAL':<20}"
                f"{total}"
            )

        self.report["verification"] = verification

        self.logger.info(
            "Dataset verification completed."
        )

    # =====================================================
    # DATASET COMPARISON
    # =====================================================

    def compare_before_after(self):
        """
        Compare processed and augmented datasets.
        """

        print()

        print("=" * 60)

        print("Dataset Comparison")

        print("=" * 60)

        comparison = {}

        splits = [
            "train",
            "validation",
            "test"
        ]

        classes = [
            "good",
            "broken_large",
            "broken_small",
            "contamination"
        ]

        for split in splits:

            comparison[split] = {}

            print()

            print(split.upper())

            for class_name in classes:

                before = len(
                    get_image_files(
                        self.input_dataset /
                        split /
                        class_name
                    )
                )

                after = len(
                    get_image_files(
                        self.output_dataset /
                        split /
                        class_name
                    )
                )

                comparison[split][class_name] = {
                    "before": before,
                    "after": after
                }

                print(
                    f"{class_name:<20}"
                    f"{before:>4}"
                    f"  --->  "
                    f"{after}"
                )

        self.report["comparison"] = comparison

    # =====================================================
    # UPDATE REPORT
    # =====================================================

    def update_report(self):
        """
        Update report metadata.
        """

        self.report["configuration"] = {
            "train_target": self.train_target,
            "validation_target": self.validation_target,
            "test_target": self.test_target
        }

        self.report["generated_at"] = str(
            datetime.now()
        )

    # =====================================================
    # EXPORT REPORT
    # =====================================================

    def export_report(self):
        """
        Export augmentation report.
        """

        output = (
            settings.REPORTS_PATH /
            "augmentation_report.json"
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.report,
                file,
                indent=4
            )

        self.logger.info(
            "Augmentation report exported."
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):
        """
        Display execution summary.
        """

        print()

        print("=" * 60)

        print("Summary")

        print("=" * 60)

        print()

        print(
            f"Train Target      : "
            f"{self.train_target}"
        )

        print(
            f"Validation Target : "
            f"{self.validation_target}"
        )

        print(
            f"Test Target       : "
            f"{self.test_target}"
        )

        print()

        print(
            f"Output Dataset : "
            f"{self.output_dataset}"
        )

        print()

        print(
            f"Report : "
            f"{settings.REPORTS_PATH}"
        )

        print()

        self.logger.info(
            "Summary generated."
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(self):
        """
        Execute complete augmentation pipeline.
        """

        start_time = datetime.now()

        try:

            self.print_header()

            self.validate_dataset()

            self.initialize_report()

            self.create_output_structure()

            self.pipeline = self.build_pipeline()

            self.augment_train()

            self.balance_validation()

            self.balance_test()

            self.verify_dataset()

            self.compare_before_after()

            self.update_report()

            self.export_report()

            self.summary()

            duration = datetime.now() - start_time

            print()

            print("=" * 60)

            print("Data Augmentation Completed Successfully")

            print("=" * 60)

            print()

            print(f"Execution Time : {duration}")

            print()

            print(
                f"Augmented Dataset : "
                f"{self.output_dataset}"
            )

            print()

            print(
                f"Report : "
                f"{settings.REPORTS_PATH}"
            )

            print()

            self.logger.info(
                "Data augmentation completed successfully."
            )

        except Exception as error:

            self.logger.exception(
                "Data augmentation failed."
            )

            raise


# =====================================================
# MAIN
# =====================================================

def main():

    augmenter = ImageAugmenter()

    augmenter.run()


if __name__ == "__main__":

    main()
