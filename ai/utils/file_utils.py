"""
============================================================
Project : VisionInspectAI
File    : file_utils.py
Author  : Aymen Chiab

Description:
    Utility functions for file and directory management.
============================================================
"""

from pathlib import Path
import shutil
from typing import List

from ai.config.config import settings


# ==========================================================
# DIRECTORY FUNCTIONS
# ==========================================================

def create_directory(directory: Path) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory (Path): Directory path.
    """
    directory.mkdir(parents=True, exist_ok=True)


ensure_directory = create_directory


def delete_directory(directory: Path) -> None:
    """
    Delete a directory and all its contents.

    Args:
        directory (Path): Directory path.
    """
    if directory.exists():
        shutil.rmtree(directory)


# ==========================================================
# FILE FUNCTIONS
# ==========================================================

def file_exists(file_path: Path) -> bool:
    """
    Check if a file exists.

    Args:
        file_path (Path): File path.

    Returns:
        bool
    """
    return file_path.exists()


def copy_file(source: Path, destination: Path) -> None:
    """
    Copy a file.

    Args:
        source (Path): Source file.
        destination (Path): Destination file.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def move_file(source: Path, destination: Path) -> None:
    """
    Move a file.

    Args:
        source (Path): Source file.
        destination (Path): Destination file.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))


def delete_file(file_path: Path) -> None:
    """
    Delete a file.

    Args:
        file_path (Path): File path.
    """
    if file_path.exists():
        file_path.unlink()


# ==========================================================
# IMAGE FUNCTIONS
# ==========================================================

def is_image_file(file_path: Path) -> bool:
    """
    Check whether a file is an image.

    Args:
        file_path (Path)

    Returns:
        bool
    """
    return file_path.suffix.lower() in settings.ALLOWED_EXTENSIONS


def get_image_files(directory: Path) -> List[Path]:
    """
    Get all image files recursively.

    Args:
        directory (Path)

    Returns:
        List[Path]
    """
    image_files = []

    for file in directory.rglob("*"):

        if file.is_file() and is_image_file(file):
            image_files.append(file)

    return sorted(image_files)


def count_images(directory: Path) -> int:
    """
    Count images inside a directory.

    Args:
        directory (Path)

    Returns:
        int
    """
    return len(get_image_files(directory))


# ==========================================================
# DIRECTORY ANALYSIS
# ==========================================================

def list_subdirectories(directory: Path) -> List[Path]:
    """
    Return all subdirectories.

    Args:
        directory (Path)

    Returns:
        List[Path]
    """
    return sorted(
        [folder for folder in directory.iterdir() if folder.is_dir()]
    )


def get_directory_size(directory: Path) -> float:
    """
    Calculate directory size in MB.

    Args:
        directory (Path)

    Returns:
        float
    """
    total_size = 0

    for file in directory.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size

    return total_size / (1024 * 1024)


# ==========================================================
# REPORT FUNCTIONS
# ==========================================================

def print_separator(length: int = 60) -> None:
    """
    Print a separator line.

    Args:
        length (int)
    """
    print("=" * length)


def print_title(title: str) -> None:
    """
    Print a formatted title.

    Args:
        title (str)
    """
    print_separator()
    print(title)
    print_separator()


# ==========================================================
# DEBUG
# ==========================================================

if __name__ == "__main__":

    print_title("VisionInspectAI - File Utilities")

    dataset = settings.BOTTLE_DATASET_PATH

    print(f"Dataset path : {dataset}")
    print(f"Exists       : {dataset.exists()}")

    if dataset.exists():
        print(f"Images       : {count_images(dataset)}")
        print(f"Size (MB)    : {get_directory_size(dataset):.2f}")