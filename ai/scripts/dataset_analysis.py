"""
============================================================
Project : VisionInspectAI
File    : dataset_analysis.py
Author  : Aymen Chiab

Description:
    Professional Dataset Analyzer for MVTec Bottle Dataset.

Features:
    - Dataset structure analysis
    - Image statistics
    - Format analysis
    - Dimension analysis
    - Duplicate detection
    - Corrupted image detection
    - Automatic report generation
============================================================
"""

from __future__ import annotations

import json
import logging
import hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from ai.config.config import settings
from ai.utils.file_utils import (
    get_image_files,
    list_subdirectories,
    count_images,
    print_separator,
)

from ai.utils.image_utils import (
    load_image,
    get_image_size,
    get_image_mode,
    get_image_channels,
    is_corrupted_image,
)


class DatasetAnalyzer:
    """
    Professional Dataset Analyzer.

    This class analyzes the Bottle dataset before
    preprocessing and training.

    It generates statistics, charts and reports.
    """

    def __init__(self):

        self.dataset_path = settings.BOTTLE_DATASET_PATH

        self.train_path = self.dataset_path / "train"

        self.test_path = self.dataset_path / "test"

        self.report = {}

        self.images = []

        self.image_sizes = []

        self.image_modes = []

        self.image_channels = []

        self.image_formats = Counter()

        self.class_distribution = {}

        self.corrupted_images = []

        self.duplicate_images = []

        self.hashes = {}

        self.total_images = 0

        self.logger = self.setup_logger()

        self.logger.info("Dataset Analyzer initialized.")
        # ======================================================
    # LOGGER
    # ======================================================

    def setup_logger(self) -> logging.Logger:
        """
        Configure application logger.
        """

        logger = logging.getLogger("DatasetAnalyzer")

        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            settings.DATASET_LOG,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        return logger

    # ======================================================
    # HEADER
    # ======================================================

    def print_header(self):

        print_separator()

        print("VisionInspectAI")

        print("Professional Dataset Analyzer")

        print_separator()

        print(f"Dataset : {self.dataset_path}")

        print()

    # ======================================================
    # DATASET VALIDATION
    # ======================================================

    def validate_dataset(self):

        self.logger.info("Checking dataset...")

        if not self.dataset_path.exists():

            raise FileNotFoundError(
                f"Dataset not found : {self.dataset_path}"
            )

        if not self.train_path.exists():

            raise FileNotFoundError(
                "Train folder not found."
            )

        if not self.test_path.exists():

            raise FileNotFoundError(
                "Test folder not found."
            )

        self.logger.info("Dataset validated successfully.")

    # ======================================================
    # REPORT INITIALIZATION
    # ======================================================

    def initialize_report(self):

        self.report = {

            "project": settings.PROJECT_NAME,

            "generated_at": str(datetime.now()),

            "dataset": str(self.dataset_path),

            "classes": {},

            "statistics": {},

            "formats": {},

            "image_sizes": {},

            "image_modes": {},

            "channels": {},

            "duplicates": [],

            "corrupted_images": []

        }

        self.logger.info("Report initialized.")
        # ======================================================
    # IMAGE COLLECTION
    # ======================================================

    def collect_images(self) -> None:
        """
        Collect all images from train and test folders.
        Ground truth masks are ignored.
        """

        self.logger.info("Collecting images...")

        self.images.clear()

        for folder in [self.train_path, self.test_path]:

            image_files = get_image_files(folder)

            self.images.extend(image_files)

        self.total_images = len(self.images)

        self.logger.info(
            "Collected %d images.",
            self.total_images
        )

    # ======================================================
    # DATASET STRUCTURE
    # ======================================================

    def analyze_structure(self) -> None:
        """
        Display dataset structure.
        """

        self.logger.info("Analyzing structure...")

        print_separator()

        print("Dataset Structure")

        print_separator()

        print("Bottle")

        print("├── train")

        for folder in list_subdirectories(self.train_path):
            print(f"│   └── {folder.name}")

        print("│")

        print("└── test")

        for folder in list_subdirectories(self.test_path):
            print(f"    └── {folder.name}")

        self.logger.info("Structure analysis completed.")
        # ======================================================
    # CLASS ANALYSIS
    # ======================================================

    def analyze_classes(self) -> None:
        """
        Count images in every class.
        """

        self.logger.info("Analyzing classes...")

        self.class_distribution.clear()

        # Train

        for folder in list_subdirectories(self.train_path):

            self.class_distribution[
                f"train/{folder.name}"
            ] = count_images(folder)

        # Test

        for folder in list_subdirectories(self.test_path):

            self.class_distribution[
                f"test/{folder.name}"
            ] = count_images(folder)

        self.report["classes"] = self.class_distribution

        print_separator()

        print("Class Distribution")

        print_separator()

        for name, count in self.class_distribution.items():

            print(f"{name:<30}{count:>6}")

        print()

        print(f"Total Images : {self.total_images}")

        self.logger.info("Class analysis completed.")
        # ======================================================
    # FORMAT ANALYSIS
    # ======================================================

    def analyze_formats(self) -> None:
        """
        Analyze image extensions.
        """

        self.logger.info("Analyzing image formats...")

        self.image_formats.clear()

        for image_path in self.images:

            extension = image_path.suffix.lower()

            self.image_formats[extension] += 1

        self.report["formats"] = dict(self.image_formats)

        print_separator()

        print("Image Formats")

        print_separator()

        for extension, count in self.image_formats.items():

            percentage = (
                count / self.total_images
            ) * 100

            print(
                f"{extension:<8}"
                f"{count:>5}"
                f" ({percentage:.1f}%)"
            )

        self.logger.info(
            "Image format analysis completed."
        )
        # ======================================================
    # IMAGE ANALYSIS
    # ======================================================

    def analyze_images(self) -> None:
        """
        Analyze every collected image.
        """

        self.logger.info("Analyzing images...")

        self.image_sizes.clear()
        self.image_modes.clear()
        self.image_channels.clear()
        self.corrupted_images.clear()

        for image_path in tqdm(
            self.images,
            desc="Analyzing images",
            unit="image"
        ):

            if is_corrupted_image(image_path):

                self.corrupted_images.append(str(image_path))

                continue

            image = load_image(image_path)

            width, height = get_image_size(image_path)

            mode = get_image_mode(image_path)

            channels = get_image_channels(image)

            self.image_sizes.append((width, height))

            self.image_modes.append(mode)

            self.image_channels.append(channels)

        self.logger.info("Image analysis completed.")
        # ======================================================
    # IMAGE DIMENSIONS
    # ======================================================

    def analyze_dimensions(self) -> None:
        """
        Analyze image dimensions.
        """

        widths = [size[0] for size in self.image_sizes]

        heights = [size[1] for size in self.image_sizes]

        self.report["image_sizes"] = {

            "min_width": min(widths),

            "max_width": max(widths),

            "mean_width": round(sum(widths) / len(widths), 2),

            "min_height": min(heights),

            "max_height": max(heights),

            "mean_height": round(sum(heights) / len(heights), 2)

        }

        print_separator()

        print("Image Dimensions")

        print_separator()

        print(f"Min Width  : {min(widths)}")

        print(f"Max Width  : {max(widths)}")

        print(f"Mean Width : {sum(widths)/len(widths):.2f}")

        print()

        print(f"Min Height : {min(heights)}")

        print(f"Max Height : {max(heights)}")

        print(f"Mean Height: {sum(heights)/len(heights):.2f}")
        # ======================================================
    # IMAGE MODES
    # ======================================================

    def analyze_modes(self) -> None:

        modes = Counter(self.image_modes)

        self.report["image_modes"] = dict(modes)

        print_separator()

        print("Image Modes")

        print_separator()

        for mode, count in modes.items():

            print(f"{mode:<10}{count}")

    # ======================================================
    # IMAGE CHANNELS
    # ======================================================

    def analyze_channels(self) -> None:

        channels = Counter(self.image_channels)

        self.report["channels"] = dict(channels)

        print_separator()

        print("Image Channels")

        print_separator()

        for channel, count in channels.items():

            print(f"{channel} channel(s) : {count}")
        # ======================================================
    # CORRUPTED IMAGES
    # ======================================================

    def analyze_corrupted(self) -> None:

        self.report["corrupted_images"] = self.corrupted_images

        print_separator()

        print("Corrupted Images")

        print_separator()

        print(f"Corrupted : {len(self.corrupted_images)}")

    # ======================================================
    # DUPLICATE IMAGES
    # ======================================================

    def analyze_duplicates(self) -> None:

        self.logger.info("Searching duplicates...")

        self.hashes.clear()

        self.duplicate_images.clear()

        for image_path in tqdm(
            self.images,
            desc="Hashing images",
            unit="image"
        ):

            with open(image_path, "rb") as file:

                image_hash = hashlib.sha256(
                    file.read()
                ).hexdigest()

            if image_hash in self.hashes:

                self.duplicate_images.append(
                    str(image_path)
                )

            else:

                self.hashes[image_hash] = image_path

        self.report["duplicates"] = self.duplicate_images

        print_separator()

        print("Duplicate Images")

        print_separator()

        print(f"Duplicates : {len(self.duplicate_images)}")
        # ======================================================
    # GLOBAL STATISTICS
    # ======================================================

    def analyze_statistics(self) -> None:

        self.report["statistics"] = {

            "total_images": self.total_images,

            "valid_images": (
                self.total_images
                - len(self.corrupted_images)
            ),

            "corrupted_images": len(
                self.corrupted_images
            ),

            "duplicate_images": len(
                self.duplicate_images
            )

        }

        print_separator()

        print("Statistics")

        print_separator()

        print(f"Total Images      : {self.total_images}")

        print(
            f"Valid Images      : "
            f"{self.total_images-len(self.corrupted_images)}"
        )

        print(
            f"Corrupted Images  : "
            f"{len(self.corrupted_images)}"
        )

        print(
            f"Duplicate Images  : "
            f"{len(self.duplicate_images)}"
        )    
        # ======================================================
    # CLASS DISTRIBUTION FIGURE
    # ======================================================

    def generate_class_distribution_figure(self) -> None:
        """
        Generate class distribution bar chart.
        """

        self.logger.info("Generating class distribution figure...")

        classes = list(self.class_distribution.keys())
        counts = list(self.class_distribution.values())

        plt.figure(figsize=(10, 6))

        plt.bar(classes, counts)

        plt.title("Class Distribution")

        plt.xlabel("Classes")

        plt.ylabel("Images")

        plt.xticks(rotation=30)

        plt.tight_layout()

        output = (
            settings.FIGURES_PATH /
            "class_distribution.png"
        )

        plt.savefig(output, dpi=300)

        plt.close()

        self.logger.info("Class distribution figure saved.")


    # ======================================================
    # IMAGE FORMAT FIGURE
    # ======================================================

    def generate_image_format_figure(self) -> None:
        """
        Generate pie chart of image formats.
        """

        plt.figure(figsize=(6, 6))

        plt.pie(
            self.image_formats.values(),
            labels=self.image_formats.keys(),
            autopct="%1.1f%%"
        )

        plt.title("Image Formats")

        plt.savefig(
            settings.FIGURES_PATH /
            "image_formats.png",
            dpi=300
        )

        plt.close()


    # ======================================================
    # IMAGE MODE FIGURE
    # ======================================================

    def generate_image_mode_figure(self) -> None:

        modes = Counter(self.image_modes)

        plt.figure(figsize=(6, 6))

        plt.bar(
            modes.keys(),
            modes.values()
        )

        plt.title("Image Modes")

        plt.savefig(
            settings.FIGURES_PATH /
            "image_modes.png",
            dpi=300
        )

        plt.close()


    # ======================================================
    # CHANNEL FIGURE
    # ======================================================

    def generate_channel_figure(self) -> None:

        channels = Counter(self.image_channels)

        plt.figure(figsize=(6, 6))

        plt.bar(
            [str(x) for x in channels.keys()],
            channels.values()
        )

        plt.title("Image Channels")

        plt.xlabel("Channels")

        plt.ylabel("Images")

        plt.savefig(
            settings.FIGURES_PATH /
            "image_channels.png",
            dpi=300
        )

        plt.close()
        # ======================================================
    # IMAGE SIZE HISTOGRAM
    # ======================================================

    def generate_image_size_figure(self) -> None:
        """
        Generate histogram of image widths.
        """

        widths = [
            size[0]
            for size in self.image_sizes
        ]

        plt.figure(figsize=(8, 5))

        plt.hist(
            widths,
            bins=20
        )

        plt.title("Image Width Distribution")

        plt.xlabel("Width")

        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(
            settings.FIGURES_PATH /
            "image_sizes.png",
            dpi=300
        )

        plt.close()

        self.logger.info("Image size figure saved.")
        # ======================================================
    # EXPORT JSON
    # ======================================================

    def export_json(self) -> None:
        """
        Export analysis report to JSON.
        """

        self.logger.info("Saving JSON report...")

        output = (
            settings.REPORTS_PATH /
            "dataset_report.json"
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

        self.logger.info("JSON report saved.")
        # ======================================================
    # EXPORT TXT
    # ======================================================

    def export_txt(self) -> None:

        output = (
            settings.REPORTS_PATH /
            "dataset_summary.txt"
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 60 + "\n")

            file.write(
                "VisionInspectAI Dataset Report\n"
            )

            file.write("=" * 60 + "\n\n")

            file.write(
                f"Dataset : {self.dataset_path}\n\n"
            )

            file.write(
                f"Total Images : {self.total_images}\n\n"
            )

            file.write("Classes\n")

            file.write("-" * 40 + "\n")

            for name, count in self.class_distribution.items():

                file.write(
                    f"{name:<30}{count}\n"
                )

            file.write("\n")

            file.write(
                f"Corrupted Images : {len(self.corrupted_images)}\n"
            )

            file.write(
                f"Duplicate Images : {len(self.duplicate_images)}\n"
            )

            file.write(
                f"Generated : {datetime.now()}\n"
            )

        self.logger.info("TXT report saved.")
        # ======================================================
    # EXPORT CSV
    # ======================================================

    def export_csv(self) -> None:

        rows = []

        for name, count in self.class_distribution.items():

            rows.append({

                "Class": name,

                "Images": count

            })

        dataframe = pd.DataFrame(rows)

        dataframe.to_csv(

            settings.REPORTS_PATH /
            "dataset_statistics.csv",

            index=False

        )

        self.logger.info("CSV report saved.")
        # ======================================================
    # RUN ANALYSIS
    # ======================================================

    def run(self) -> None:
        """
        Execute the complete analysis pipeline.
        """

        start_time = datetime.now()

        try:

            self.print_header()

            self.validate_dataset()

            self.initialize_report()

            self.collect_images()

            self.analyze_structure()

            self.analyze_classes()

            self.analyze_formats()

            self.analyze_images()

            self.analyze_dimensions()

            self.analyze_modes()

            self.analyze_channels()

            self.analyze_corrupted()

            self.analyze_duplicates()

            self.analyze_statistics()

            # -----------------------------
            # Generate figures
            # -----------------------------

            self.generate_class_distribution_figure()

            self.generate_image_format_figure()

            self.generate_image_mode_figure()

            self.generate_channel_figure()

            self.generate_image_size_figure()

            # -----------------------------
            # Export reports
            # -----------------------------

            self.export_json()

            self.export_txt()

            self.export_csv()

            duration = datetime.now() - start_time

            print_separator()

            print("Analysis completed successfully!")

            print_separator()

            print(f"Images analyzed : {self.total_images}")

            print(
                f"Corrupted images : "
                f"{len(self.corrupted_images)}"
            )

            print(
                f"Duplicate images : "
                f"{len(self.duplicate_images)}"
            )

            print(f"Execution time : {duration}")

            print()

            print(
                f"Reports : {settings.REPORTS_PATH}"
            )

            print(
                f"Figures : {settings.FIGURES_PATH}"
            )

            self.logger.info(
                "Dataset analysis completed successfully."
            )

        except Exception as error:

            self.logger.exception(error)

            raise
# ======================================================
# MAIN
# ======================================================

def main():

    analyzer = DatasetAnalyzer()

    analyzer.run()


if __name__ == "__main__":

    main()                                                                    