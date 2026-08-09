"""
============================================================
Project : VisionInspectAI
File    : image_utils.py
Author  : Aymen Chiab

Description:
    Utility functions for image loading, validation,
    preprocessing and visualization.
============================================================
"""

from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
import shutil

from ai.config.config import settings


# ==========================================================
# IMAGE LOADING
# ==========================================================

def load_image(image_path: Path) -> np.ndarray:
    """
    Load an image using OpenCV.

    Args:
        image_path (Path): Image path.

    Returns:
        np.ndarray
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Cannot load image : {image_path}")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


def load_pil_image(image_path: Path) -> Image.Image:
    """
    Load image using Pillow.

    Args:
        image_path (Path)

    Returns:
        PIL.Image
    """

    return Image.open(image_path)


# ==========================================================
# IMAGE VALIDATION
# ==========================================================

def is_corrupted_image(image_path: Path) -> bool:
    """
    Check if an image is corrupted.

    Args:
        image_path (Path)

    Returns:
        bool
    """

    try:
        with Image.open(image_path) as img:
            img.verify()

        return False

    except Exception:
        return True


# ==========================================================
# IMAGE INFORMATION
# ==========================================================

def get_image_size(image_path: Path) -> Tuple[int, int]:
    """
    Return image size.

    Args:
        image_path (Path)

    Returns:
        Tuple(width, height)
    """

    with Image.open(image_path) as img:
        return img.size


def get_image_mode(image_path: Path) -> str:
    """
    Return image mode.

    Examples:
        RGB
        RGBA
        L

    Args:
        image_path (Path)

    Returns:
        str
    """

    with Image.open(image_path) as img:
        return img.mode


def get_image_channels(image: np.ndarray) -> int:
    """
    Return number of image channels.

    Args:
        image (np.ndarray)

    Returns:
        int
    """

    if len(image.shape) == 2:
        return 1

    return image.shape[2]


# ==========================================================
# IMAGE PROCESSING
# ==========================================================

def resize_image(image: np.ndarray) -> np.ndarray:
    """
    Resize image to configured size.

    Args:
        image (np.ndarray)

    Returns:
        np.ndarray
    """

    return cv2.resize(
        image,
        settings.IMAGE_SIZE,
        interpolation=cv2.INTER_AREA
    )


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image pixels between 0 and 1.

    Args:
        image (np.ndarray)

    Returns:
        np.ndarray
    """

    return image.astype(np.float32) / 255.0


def preprocess_image(image_path: Path) -> np.ndarray:
    """
    Complete preprocessing pipeline.

    Args:
        image_path (Path)

    Returns:
        np.ndarray
    """

    image = load_image(image_path)

    image = resize_image(image)

    image = normalize_image(image)

    return image


# ==========================================================
# IMAGE STATISTICS
# ==========================================================

def get_image_statistics(image: np.ndarray) -> dict:
    """
    Compute image statistics.

    Args:
        image (np.ndarray)

    Returns:
        dict
    """

    return {
        "height": image.shape[0],
        "width": image.shape[1],
        "channels": get_image_channels(image),
        "min": float(np.min(image)),
        "max": float(np.max(image)),
        "mean": float(np.mean(image)),
        "std": float(np.std(image))
    }


# ==========================================================
# SAVE IMAGE
# ==========================================================

def copy_image(source: Path, destination: Path) -> None:
    """
    Copy an image file.

    Args:
        source (Path): Source image path.
        destination (Path): Destination image path.
    """

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def save_image(image: np.ndarray, output_path: Path) -> None:
    """
    Save image.

    Args:
        image (np.ndarray)
        output_path (Path)
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.imwrite(str(output_path), image_bgr)


# ==========================================================
# DEBUG
# ==========================================================

if __name__ == "__main__":

    sample_directory = (
        settings.BOTTLE_DATASET_PATH /
        "train" /
        "good"
    )

    image_files = list(sample_directory.glob("*.png"))

    if image_files:

        image_path = image_files[0]

        image = load_image(image_path)

        print("=" * 60)
        print("VisionInspectAI - Image Utilities")
        print("=" * 60)
        print(f"Image        : {image_path.name}")
        print(f"Size         : {get_image_size(image_path)}")
        print(f"Mode         : {get_image_mode(image_path)}")
        print(f"Channels     : {get_image_channels(image)}")
        print(f"Statistics   : {get_image_statistics(image)}")
        print("=" * 60)