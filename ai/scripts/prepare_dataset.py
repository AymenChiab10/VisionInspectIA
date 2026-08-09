"""
============================================================
Project : VisionInspectAI
File    : prepare_dataset.py
Author  : Aymen Chiab

Description:
    Prepare the MVTec Bottle dataset for image classification.

Features:
    - Dataset validation
    - Train / Validation / Test split
    - Copy images
    - Report generation
============================================================
"""

from __future__ import annotations

import json
import logging
import random
import shutil

from datetime import datetime
from pathlib import Path

from ai.config.config import settings
from typing import Dict, List
from tqdm import tqdm

from ai.utils.file_utils import (
    create_directory,
    get_image_files,
    print_separator,
)
class DatasetPreparer:

    def __init__(self):

        self.raw_dataset = settings.BOTTLE_DATASET_PATH

        self.output_dataset = settings.PROCESSED_DATA_PATH / "bottle"

        self.train_path = self.raw_dataset / "train"

        self.test_path = self.raw_dataset / "test"

        self.report = {}

        self.logger = self.setup_logger()

        random.seed(settings.RANDOM_SEED)

        self.logger.info("DatasetPreparer initialized.")
        # =====================================================
    # LOGGER
    # =====================================================

    def setup_logger(self):

        logger = logging.getLogger("DatasetPreparer")

        logger.setLevel(logging.INFO)

        if logger.handlers:

            return logger

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        file_handler = logging.FileHandler(

            settings.LOGS_PATH / "prepare_dataset.log",

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

        print_separator()

        print("VisionInspectAI")

        print("Dataset Preparation")

        print_separator()

        print(f"Input Dataset : {self.raw_dataset}")

        print(f"Output Dataset : {self.output_dataset}")

        print()
        # =====================================================
    # VALIDATION
    # =====================================================

    def validate_dataset(self):

        self.logger.info("Checking dataset...")

        if not self.raw_dataset.exists():

            raise FileNotFoundError(

                self.raw_dataset

            )

        if not self.train_path.exists():

            raise FileNotFoundError(

                self.train_path

            )

        if not self.test_path.exists():

            raise FileNotFoundError(

                self.test_path

            )

        self.logger.info("Dataset validated.")
        # =====================================================
    # REPORT
    # =====================================================

    def initialize_report(self):

        self.report = {

            "project": settings.PROJECT_NAME,

            "generated_at": str(datetime.now()),

            "dataset": str(self.raw_dataset),

            "splits": {},

            "classes": {}

        }

        self.logger.info("Report initialized.")
        # =====================================================
    # CREATE OUTPUT STRUCTURE
    # =====================================================

    def create_output_structure(self):

        self.logger.info("Creating folders...")

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

                create_directory(

                    self.output_dataset /

                    split /

                    cls

                )

        self.logger.info("Folders created.")
        # =====================================================
    # COLLECT IMAGES
    # =====================================================

    def collect_images(self) -> Dict[str, List[Path]]:
        """
        Collect all images by class.

        Returns:
            Dictionary containing image paths grouped by class.
        """

        self.logger.info("Collecting images...")

        images = {}

        # -----------------------------
        # GOOD IMAGES
        # -----------------------------

        train_good = self.train_path / "good"

        images["good_train"] = get_image_files(train_good)

        test_good = self.test_path / "good"

        images["good_test"] = get_image_files(test_good)

        # -----------------------------
        # DEFECT CLASSES
        # -----------------------------

        for defect in [

            "broken_large",

            "broken_small",

            "contamination"

        ]:

            folder = self.test_path / defect

            images[defect] = get_image_files(folder)

        self.logger.info("Image collection completed.")

        return images
        # =====================================================
    # SPLIT IMAGES
    # =====================================================

    def split_images(
        self,
        images: List[Path]
    ) -> tuple[list[Path], list[Path], list[Path]]:
        """
        Split images into train / validation / test.
        """

        random.shuffle(images)

        n = len(images)

        train_end = int(n * settings.TRAIN_SPLIT)

        validation_end = train_end + int(

            n * settings.VALIDATION_SPLIT

        )

        train = images[:train_end]

        validation = images[train_end:validation_end]

        test = images[validation_end:]

        return train, validation, test
        # =====================================================
    # PREPARE SPLITS
    # =====================================================

    def prepare_splits(self):

        dataset = self.collect_images()

        prepared = {}

        # -------------------------
        # GOOD
        # -------------------------

        train_good = dataset["good_train"]

        random.shuffle(train_good)

        validation_size = int(

            len(train_good)

            * settings.VALIDATION_SPLIT

        )

        prepared["good"] = {

            "train": train_good[validation_size:],

            "validation": train_good[:validation_size],

            "test": dataset["good_test"]

        }

        # -------------------------
        # DEFECTS
        # -------------------------

        for defect in [

            "broken_large",

            "broken_small",

            "contamination"

        ]:

            train, validation, test = self.split_images(

                dataset[defect]

            )

            prepared[defect] = {

                "train": train,

                "validation": validation,

                "test": test

            }

        return prepared
        # =====================================================
    # DISPLAY SPLITS
    # =====================================================

    def display_splits(self, prepared):

        print_separator()

        print("Dataset Split")

        print_separator()

        for cls, values in prepared.items():

            print(

                f"\n{cls}"

            )

            print(

                f"Train      : {len(values['train'])}"

            )

            print(

                f"Validation : {len(values['validation'])}"

            )

            print(

                f"Test       : {len(values['test'])}"

            )
        # =====================================================
    # COPY FILE
    # =====================================================

    def copy_image(
        self,
        source: Path,
        destination: Path
    ) -> None:
        """
        Copy one image to destination.
        """

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            source,
            destination
        )
        # =====================================================
    # COPY DATASET
    # =====================================================

    def copy_dataset(self, prepared):

        self.logger.info("Copying dataset...")

        total = sum(

            len(images)

            for cls in prepared.values()

            for images in cls.values()

        )

        with tqdm(

            total=total,

            desc="Copying images",

            unit="image"

        ) as progress:

            for class_name, splits in prepared.items():

                for split_name, images in splits.items():

                    destination = (

                        self.output_dataset

                        / split_name

                        / class_name

                    )

                    for image in images:

                        self.copy_image(

                            image,

                            destination / image.name

                        )

                        progress.update(1)

        self.logger.info("Dataset copied.")
        # =====================================================
    # VERIFY DATASET
    # =====================================================

    def verify_dataset(self):

        print_separator()

        print("Verification")

        print_separator()

        verification = {}

        for split in [

            "train",

            "validation",

            "test"

        ]:

            verification[split] = {}

            for cls in [

                "good",

                "broken_large",

                "broken_small",

                "contamination"

            ]:

                folder = (

                    self.output_dataset

                    / split

                    / cls

                )

                count = len(

                    get_image_files(folder)

                )

                verification[split][cls] = count

                print(

                    f"{split:<12}"

                    f"{cls:<18}"

                    f"{count}"

                )

        self.report["verification"] = verification

        self.logger.info("Verification completed.")
        # =====================================================
    # EXPORT REPORT
    # =====================================================

    def export_report(self):

        output = (

            settings.REPORTS_PATH

            / "prepare_dataset_report.json"

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

            "Preparation report saved."

        )
        # =====================================================
    # UPDATE REPORT
    # =====================================================

    def update_report(self, prepared):

        report = {}

        for cls, splits in prepared.items():

            report[cls] = {

                split: len(images)

                for split, images

                in splits.items()

            }

        self.report["splits"] = report
        # =====================================================
    # RUN
    # =====================================================

    def run(self) -> None:
        """
        Execute the complete dataset preparation pipeline.
        """

        start_time = datetime.now()

        try:

            self.print_header()

            self.validate_dataset()

            self.initialize_report()

            self.create_output_structure()

            prepared = self.prepare_splits()

            self.display_splits(prepared)

            self.update_report(prepared)

            self.copy_dataset(prepared)

            self.verify_dataset()

            self.export_report()

            duration = datetime.now() - start_time

            print_separator()

            print("Dataset preparation completed successfully!")

            print_separator()

            print(f"Execution time : {duration}")

            print()

            print(f"Dataset saved to : {self.output_dataset}")

            print(f"Report saved to  : {settings.REPORTS_PATH}")

            self.logger.info(
                "Dataset preparation completed successfully."
            )

        except Exception as error:

            self.logger.exception(error)

            raise
# =====================================================
# MAIN
# =====================================================

def main():

    preparer = DatasetPreparer()

    preparer.run()


if __name__ == "__main__":

    main()                                     