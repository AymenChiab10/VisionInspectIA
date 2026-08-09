"""
============================================================
Project : VisionInspectAI
File    : create_tf_dataset.py
Author  : Aymen Chiab

Description:
    Build TensorFlow datasets from the augmented Bottle dataset.

Features:
    - Train Dataset
    - Validation Dataset
    - Test Dataset
    - Normalization
    - Cache
    - Prefetch
============================================================
"""

from __future__ import annotations

import json
import logging

from datetime import datetime
from pathlib import Path

import tensorflow as tf

from ai.config.config import settings

from ai.utils.file_utils import (
    print_separator,
)
class DatasetLoader:

    """
    TensorFlow Dataset Loader.
    """
    def __init__(self):

        experiment = settings.EXPERIMENTS[settings.EXPERIMENT_MODE]

        self.dataset_type = experiment["dataset_type"]

        self.augmentation_enabled = experiment.get("augmentation", False)

        self.experiment_name = experiment.get("name", settings.EXPERIMENT_MODE)

        if self.dataset_type == "raw_mvtec":

            self.use_raw_mvtec = True

            self.dataset_path = settings.RAW_MVTEC_BOTTLE_PATH

            self.train_path = (
                self.dataset_path / "train" / "good"
            )

        elif self.dataset_type == "augmented":

            self.use_raw_mvtec = False

            self.dataset_path = settings.AUGMENTED_BOTTLE_PATH

            self.train_path = experiment["train_path"]

        else:

            raise ValueError(
                f"Unknown dataset_type: {self.dataset_type}"
            )

        self.validation_path = settings.SHARED_VALIDATION_PATH

        self.test_path = settings.SHARED_TEST_PATH

        if self.augmentation_enabled:

            self.augmentation = self.build_augmentation()

        else:

            self.augmentation = None

        self.logger = self.setup_logger()

        self.report = {}

        self.class_names = []

        self.train_dataset = None

        self.validation_dataset = None

        self.test_dataset = None

        self.logger.info(

            "DatasetLoader initialized."

        )
        # =====================================================
    # LOGGER
    # =====================================================

    def setup_logger(self):

        logger = logging.getLogger(

            "DatasetLoader"

        )

        logger.setLevel(

            logging.INFO

        )

        if logger.handlers:

            return logger

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        file_handler = logging.FileHandler(

            settings.LOGS_PATH /

            "create_tf_dataset.log",

            encoding="utf-8"

        )

        file_handler.setFormatter(

            formatter

        )

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(

            formatter

        )

        logger.addHandler(

            file_handler

        )

        logger.addHandler(

            console_handler

        )

        return logger
        # =====================================================
    # HEADER
    # =====================================================

    def print_header(self):

        print_separator()

        print("VisionInspectAI")

        print("TensorFlow Dataset Loader")

        print_separator()

        print(

            f"Dataset : "

            f"{self.dataset_path}"

        )

        print()
        # =====================================================
    # VALIDATION
    # =====================================================

    def validate_dataset(self):

        self.logger.info(
            "Checking dataset..."
        )

        if self.use_raw_mvtec:

            if not self.dataset_path.exists():

                raise FileNotFoundError(
                    f"Raw MVTec dataset not found: {self.dataset_path}"
                )

            if not self.train_path.exists():

                raise FileNotFoundError(
                    f"Train path not found: {self.train_path}"
                )

            if not self.test_path.exists():

                raise FileNotFoundError(
                    f"Test path not found: {self.test_path}"
                )

        else:

            for folder in [

                self.train_path,

                self.validation_path,

                self.test_path

            ]:

                if not folder.exists():

                    raise FileNotFoundError(
                        folder
                    )

        self.logger.info(
            "Dataset validated."
        )
        # =====================================================
    # REPORT
    # =====================================================

    def initialize_report(self):

        self.report = {

            "project": settings.PROJECT_NAME,

            "generated_at": str(

                datetime.now()

            ),

            "dataset": str(

                self.dataset_path

            ),

            "classes": [],

            "batch_size": settings.BATCH_SIZE,

            "image_size": list(

                settings.IMAGE_SIZE

            )

        }

        self.logger.info(

            "Report initialized."
        )

    # =====================================================
    # AUGMENTATION
    # =====================================================

    @staticmethod
    def build_augmentation():
        """
        Build on-the-fly augmentation pipeline for training.
        """

        return tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip(
                    mode=settings.RANDOM_FLIP_MODE,
                    seed=settings.DATASET_SEED,
                ),
                tf.keras.layers.RandomRotation(
                    factor=settings.RANDOM_ROTATION_FACTOR,
                    seed=settings.DATASET_SEED,
                ),
                tf.keras.layers.RandomZoom(
                    height_factor=settings.RANDOM_ZOOM_HEIGHT,
                    width_factor=settings.RANDOM_ZOOM_WIDTH,
                    seed=settings.DATASET_SEED,
                ),
                tf.keras.layers.RandomTranslation(
                    height_factor=settings.RANDOM_TRANSLATION_HEIGHT,
                    width_factor=settings.RANDOM_TRANSLATION_WIDTH,
                    seed=settings.DATASET_SEED,
                ),
                tf.keras.layers.RandomContrast(
                    factor=settings.RANDOM_CONTRAST_FACTOR,
                    seed=settings.DATASET_SEED,
                ),
            ],
            name="on_the_fly_augmentation",
        )

    @staticmethod
    def _compute_file_hash(path: Path) -> str:
        """
        Compute MD5 hash of a file for duplicate detection.
        """

        import hashlib

        hasher = hashlib.md5()

        with open(path, "rb") as file:
            hasher.update(file.read())

        return hasher.hexdigest()

    @staticmethod
    def augment(images, labels):
        """
        Apply augmentation to a batch of images.
        """

        return images, labels
        # =====================================================
    # CONFIGURE DATASET
    # =====================================================

    def configure_dataset(
        self,
        dataset: tf.data.Dataset,
        training: bool = False
    ) -> tf.data.Dataset:
        """
        Configure TensorFlow dataset.

        Parameters
        ----------
        dataset : tf.data.Dataset
            Dataset to configure.

        training : bool
            True only for the training dataset.

        Returns
        -------
        tf.data.Dataset
            Optimized dataset.
        """

        # -----------------------------------------
        # On-the-fly augmentation (training only)
        # -----------------------------------------

        if training and self.augmentation_enabled and self.augmentation is not None:

            dataset = dataset.map(
                lambda images, labels: (self.augmentation(images, training=True), labels),
                num_parallel_calls=tf.data.AUTOTUNE,
            )

        # -----------------------------------------
        # Cache
        # -----------------------------------------

        if settings.CACHE_DATASET:

            dataset = dataset.cache()

        # -----------------------------------------
        # Shuffle (training only)
        # -----------------------------------------

        if training and settings.SHUFFLE:

            dataset = dataset.shuffle(
                buffer_size=1000,
                seed=settings.DATASET_SEED,
                reshuffle_each_iteration=True,
            )

        # -----------------------------------------
        # Prefetch
        # -----------------------------------------

        if settings.PREFETCH_DATASET:

            dataset = dataset.prefetch(
                tf.data.AUTOTUNE
            )

        return dataset
        # =====================================================
    # TRAIN DATASET
    # =====================================================

    def create_train_dataset(self) -> None:
        """
        Create TensorFlow training dataset.
        """

        self.logger.info("Creating training dataset...")

        self.train_dataset = tf.keras.utils.image_dataset_from_directory(

            self.train_path,

            labels="inferred",

            label_mode="int",

            batch_size=settings.BATCH_SIZE,

            image_size=settings.IMAGE_SIZE,

            shuffle=True,

            seed=settings.DATASET_SEED,

        )

        self.class_names = self.train_dataset.class_names

        self.train_dataset = self.configure_dataset(
        self.train_dataset,
        training=True
)
        self.logger.info("Training dataset created.")
        # =====================================================
    # VALIDATION DATASET
    # =====================================================

    def create_validation_dataset(self) -> None:
        """
        Create TensorFlow validation dataset.
        """

        self.logger.info("Creating validation dataset...")

        self.validation_dataset = tf.keras.utils.image_dataset_from_directory(

            self.validation_path,

            labels="inferred",

            label_mode="int",

            batch_size=settings.BATCH_SIZE,

            image_size=settings.IMAGE_SIZE,

            shuffle=False

        )

        self.validation_dataset = self.configure_dataset(
        self.validation_dataset,
        training=False
)

        self.logger.info("Validation dataset created.")
        # =====================================================
    # TEST DATASET
    # =====================================================

    def create_test_dataset(self) -> None:
        """
        Create TensorFlow test dataset.
        """

        self.logger.info("Creating test dataset...")

        self.test_dataset = tf.keras.utils.image_dataset_from_directory(

            self.test_path,

            labels="inferred",

            label_mode="int",

            batch_size=settings.BATCH_SIZE,

            image_size=settings.IMAGE_SIZE,

            shuffle=False

        )

        self.test_dataset = self.configure_dataset(
        self.test_dataset,
        training=False
        )

        self.logger.info("Test dataset created.")

    # =====================================================
    # RAW MVTEC DATASETS
    # =====================================================

    def create_raw_mvtec_datasets(self) -> None:
        """
        Create datasets from raw MVTec Bottle structure.

        Uses ALL available real images from all classes for 4-class
        classification with stratified train/validation/test split.

        Validation and test sets are loaded from shared paths to ensure
        identical evaluation across experiments.
        """

        self.logger.info(
            "Creating datasets from raw MVTec structure..."
        )

        from sklearn.model_selection import train_test_split

        class_names = [
            "broken_large",
            "broken_small",
            "contamination",
            "good",
        ]

        self.class_names = class_names

        label_map = {
            "broken_large": 0,
            "broken_small": 1,
            "contamination": 2,
            "good": 3,
        }

        all_images = []
        all_labels = []

        source_dirs = [
            (self.dataset_path / "train" / "good", "good"),
            (self.dataset_path / "test" / "broken_large", "broken_large"),
            (self.dataset_path / "test" / "broken_small", "broken_small"),
            (self.dataset_path / "test" / "contamination", "contamination"),
            (self.dataset_path / "test" / "good", "good"),
        ]

        excluded_files = set()

        for shared_path in [
            settings.SHARED_VALIDATION_PATH,
            settings.SHARED_TEST_PATH,
        ]:
            if not shared_path.exists():
                continue
            for image_path in shared_path.rglob("*"):
                if image_path.is_file() and image_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                    excluded_files.add(self._compute_file_hash(image_path))

        for dir_path, class_name in source_dirs:

            if not dir_path.exists():

                continue

            image_paths = sorted(
                list(dir_path.glob("*.png"))
            ) + sorted(
                list(dir_path.glob("*.jpg"))
            ) + sorted(
                list(dir_path.glob("*.jpeg"))
            )

            for image_path in image_paths:

                if self._compute_file_hash(image_path) in excluded_files:
                    continue

                all_images.append(str(image_path))
                all_labels.append(label_map[class_name])

        self.logger.info(
            f"Total real images loaded: {len(all_images)}"
        )

        for class_name in class_names:

            count = all_labels.count(
                label_map[class_name]
            )

            self.logger.info(
                f"  {class_name}: {count} images"
            )

        train_images, temp_images, train_labels, temp_labels = (
            train_test_split(
                all_images,
                all_labels,
                test_size=0.30,
                random_state=settings.DATASET_SEED,
                stratify=all_labels,
            )
        )

        val_images, test_images, val_labels, test_labels = (
            train_test_split(
                temp_images,
                temp_labels,
                test_size=0.50,
                random_state=settings.DATASET_SEED,
                stratify=temp_labels,
            )
        )

        self.logger.info(
            f"Train: {len(train_images)} images"
        )

        self.logger.info(
            f"Validation: {len(val_images)} images"
        )

        self.logger.info(
            f"Test: {len(test_images)} images"
        )

        def load_and_preprocess(image_path, label):

            image = tf.io.read_file(image_path)

            image = tf.image.decode_image(image, channels=3)

            image = tf.ensure_shape(image, [None, None, 3])

            image = tf.image.resize(image, settings.IMAGE_SIZE)

            image = tf.cast(image, tf.float32)

            image = tf.ensure_shape(
                image,
                [settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH, 3]
            )

            return image, label

        self.train_dataset = tf.data.Dataset.from_tensor_slices(
            (train_images, train_labels)
        )

        self.validation_dataset = tf.data.Dataset.from_tensor_slices(
            (val_images, val_labels)
        )

        self.test_dataset = tf.data.Dataset.from_tensor_slices(
            (test_images, test_labels)
        )

        self.train_dataset = self.train_dataset.map(
            load_and_preprocess,
            num_parallel_calls=tf.data.AUTOTUNE,
        )

        self.validation_dataset = self.validation_dataset.map(
            load_and_preprocess,
            num_parallel_calls=tf.data.AUTOTUNE,
        )

        self.test_dataset = self.test_dataset.map(
            load_and_preprocess,
            num_parallel_calls=tf.data.AUTOTUNE,
        )

        self.train_dataset = self.train_dataset.batch(
            settings.BATCH_SIZE
        )

        self.train_dataset = self.configure_dataset(
            self.train_dataset,
            training=True
        )

        self.validation_dataset = self.validation_dataset.batch(
            settings.BATCH_SIZE
        )

        self.validation_dataset = self.configure_dataset(
            self.validation_dataset,
            training=False
        )

        self.test_dataset = self.test_dataset.batch(
            settings.BATCH_SIZE
        )

        self.test_dataset = self.configure_dataset(
            self.test_dataset,
            training=False
        )

        self.logger.info("Raw MVTec datasets created.")

    # =====================================================
    # CREATE ALL DATASETS
    # =====================================================

    def create_datasets(self) -> None:
        """
        Create train, validation and test datasets.
        """

        if self.dataset_type == "raw_mvtec":

            self.create_raw_mvtec_datasets()

            self.create_validation_dataset()

            self.create_test_dataset()

        elif self.dataset_type == "augmented":

            self.create_train_dataset()

            self.create_validation_dataset()

            self.create_test_dataset()

        self.logger.info("All datasets created.")
        # =====================================================
    # DATASET INFORMATION
    # =====================================================

    def display_dataset_information(self) -> None:
        """
        Display TensorFlow dataset information.
        """

        print_separator()

        print("TensorFlow Dataset")

        print_separator()

        print()

        print("Classes")

        print("-------")

        for index, name in enumerate(self.class_names):

            print(f"{index} -> {name}")

        print()

        print(

            f"Batch Size : "

            f"{settings.BATCH_SIZE}"

        )

        print(

            f"Image Size : "

            f"{settings.IMAGE_SIZE}"

        )

        print()

        print(

            f"Train batches : "

            f"{tf.data.experimental.cardinality(self.train_dataset).numpy()}"

        )

        print(

            f"Validation batches : "

            f"{tf.data.experimental.cardinality(self.validation_dataset).numpy()}"

        )

        print(

            f"Test batches : "

            f"{tf.data.experimental.cardinality(self.test_dataset).numpy()}"

        )
        # =====================================================
    # VERIFY DATASET
    # =====================================================

    def verify_dataset(self) -> None:
        """
        Verify one batch from the training dataset.
        """

        images, labels = next(
            iter(self.train_dataset)
        )

        print_separator()

        print("Dataset Verification")

        print_separator()

        print()

        print(

            f"Images Shape : "

            f"{images.shape}"

        )

        print(

            f"Labels Shape : "

            f"{labels.shape}"

        )

        print(

            f"Images dtype : "

            f"{images.dtype}"

        )

        print(

            f"Labels dtype : "

            f"{labels.dtype}"

        )

        print(

            f"Min Pixel : "

            f"{tf.reduce_min(images).numpy():.3f}"

        )

        print(

            f"Max Pixel : "

            f"{tf.reduce_max(images).numpy():.3f}"

        )
        # =====================================================
    # UPDATE REPORT
    # =====================================================

    def update_report(self) -> None:
        """
        Update TensorFlow dataset report.
        """

        self.report["classes"] = self.class_names

        self.report["num_classes"] = len(
            self.class_names
        )

        self.report["train_batches"] = int(
            tf.data.experimental.cardinality(
                self.train_dataset
            ).numpy()
        )

        self.report["validation_batches"] = int(
            tf.data.experimental.cardinality(
                self.validation_dataset
            ).numpy()
        )

        self.report["test_batches"] = int(
            tf.data.experimental.cardinality(
                self.test_dataset
            ).numpy()
        )

        self.logger.info(
            "Report updated."
        )
        # =====================================================
    # EXPORT REPORT
    # =====================================================

    def export_report(self) -> None:
        """
        Export report to JSON.
        """

        output = (

            settings.REPORTS_PATH /

            "tf_dataset_report.json"

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

            "TensorFlow report exported."

        )
        # =====================================================
    # SAMPLE BATCH
    # =====================================================

    def display_sample_batch(self) -> None:
        """
        Display one batch information.
        """

        images, labels = next(
            iter(self.train_dataset)
        )

        print_separator()

        print("Sample Batch")

        print_separator()

        print()

        print(

            f"Images : "

            f"{images.shape}"

        )

        print(

            f"Labels : "

            f"{labels.numpy()}"

        )

        print(

            f"Min Pixel : "

            f"{tf.reduce_min(images).numpy():.3f}"

        )

        print(

            f"Max Pixel : "

            f"{tf.reduce_max(images).numpy():.3f}"

        )
       
        # =====================================================
    # RUN
    # =====================================================

    def run(self) -> None:

        start_time = datetime.now()

        try:

            self.print_header()

            self.validate_dataset()

            self.initialize_report()

            self.create_datasets()

            self.display_dataset_information()

            self.verify_dataset()

            self.display_sample_batch()

            self.update_report()

            self.export_report()

            duration = datetime.now() - start_time

            print_separator()

            print("TensorFlow Dataset Ready")

            print_separator()

            print()

            print(

                f"Execution Time : "

                f"{duration}"

            )

            print()

            print(

                f"Dataset : "

                f"{self.dataset_path}"

            )

            print(

                f"Report : "

                f"{settings.REPORTS_PATH}"

            )

            self.logger.info(

                "TensorFlow dataset ready."

            )

        except Exception as error:

            self.logger.exception(error)

            raise
# =====================================================
# MAIN
# =====================================================

def main():

    loader = DatasetLoader()

    loader.run()


if __name__ == "__main__":

    main()                    