"""
Visual error analysis for augmented balanced benchmark.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img

from ai.config.config import settings
from ai.models.model_factory import ModelFactory
from ai.models.preprocessing_layers import (
    EfficientNetPreprocess,
    MobileNetPreprocess,
    ResNetPreprocess,
)


def get_image_paths(split_dir: Path) -> dict[str, list[Path]]:
    paths = {}
    for class_dir in sorted(split_dir.iterdir()):
        if class_dir.is_dir():
            files = sorted(
                list(class_dir.glob("*.png"))
                + list(class_dir.glob("*.jpg"))
                + list(class_dir.glob("*.jpeg"))
            )
            paths[class_dir.name] = files
    return paths


def main() -> None:
    base = Path("data/augmented/bottle/test")
    test_ds = tf.keras.utils.image_dataset_from_directory(
        base,
        labels="inferred",
        label_mode="int",
        batch_size=settings.BATCH_SIZE,
        image_size=settings.IMAGE_SIZE,
        shuffle=False,
    )
    class_names = list(test_ds.class_names)
    paths_by_class = get_image_paths(base)
    flat_paths = []
    for name in class_names:
        flat_paths.extend(paths_by_class[name])
    assert len(flat_paths) == len(test_ds.file_paths), (
        f"Path count mismatch: {len(flat_paths)} vs {len(test_ds.file_paths)}"
    )

    custom_objects = {
        "MobileNetPreprocess": MobileNetPreprocess,
        "ResNetPreprocess": ResNetPreprocess,
        "EfficientNetPreprocess": EfficientNetPreprocess,
    }
    pairs = [
        ("mobilenet_v2", "mobilenet"),
        ("resnet50", "resnet"),
        ("efficientnet_b0", "efficientnet"),
    ]

    for model_name, model_type in pairs:
        settings.MODEL_TYPE = model_type
        settings.MODEL_NAME = model_name
        model = tf.keras.models.load_model(
            f"ai/saved_models/{model_name}/best_model.keras",
            custom_objects=custom_objects,
        )
        y_true, y_pred, probs = [], [], []
        for imgs, labels in test_ds:
            p = model.predict(imgs, verbose=0)
            probs.extend(p.tolist())
            y_pred.extend(np.argmax(p, axis=1).tolist())
            y_true.extend(labels.numpy().tolist())
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        probs = np.array(probs)

        correct = np.where(y_true == y_pred)[0]
        wrong = np.where(y_true != y_pred)[0]

        fig, axes = plt.subplots(2, 5, figsize=(15, 6))
        axes = axes.flatten()
        for i, idx in enumerate(correct[:5]):
            img = load_img(flat_paths[idx], target_size=(224, 224))
            axes[i].imshow(img)
            axes[i].set_title(
                f"T:{class_names[y_true[idx]]}\nP:{class_names[y_pred[idx]]}\n{probs[idx].max():.2f}",
                fontsize=8,
            )
            axes[i].axis("off")
        for i, idx in enumerate(wrong[:5]):
            img = load_img(flat_paths[idx], target_size=(224, 224))
            axes[i + 5].imshow(img)
            axes[i + 5].set_title(
                f"T:{class_names[y_true[idx]]}\nP:{class_names[y_pred[idx]]}\n{probs[idx].max():.2f}",
                fontsize=8,
            )
            axes[i + 5].axis("off")
        plt.suptitle(f"{model_name} - top correct / bottom wrong", fontsize=12)
        plt.tight_layout()
        out = Path(f"ai/results/figures/{model_name}_errors.png")
        plt.savefig(out, dpi=150)
        plt.close()
        print(f"Saved {out}")

        # Confidence distributions
        fig, axes = plt.subplots(1, 4, figsize=(15, 4))
        for i, cls in enumerate(class_names):
            mask = y_true == i
            axes[i].hist(probs[mask].max(axis=1), bins=20, alpha=0.7)
            axes[i].set_title(f"{cls}\nmean conf: {probs[mask].max(axis=1).mean():.2f}")
            axes[i].set_xlabel("Confidence")
            axes[i].set_ylabel("Count")
        plt.suptitle(f"{model_name} - confidence by true class", fontsize=12)
        plt.tight_layout()
        out = Path(f"ai/results/figures/{model_name}_confidence.png")
        plt.savefig(out, dpi=150)
        plt.close()
        print(f"Saved {out}")


if __name__ == "__main__":
    main()
