"""
============================================================
Project : VisionInspectAI
File    : metrics.py
Author  : Aymen Chiab

Description:
    Centralized Keras metrics for imbalanced
    industrial defect classification.
============================================================
"""

from __future__ import annotations

import tensorflow as tf


def get_classification_metrics() -> list[tf.keras.metrics.Metric]:
    """
    Return standard classification metrics for
    imbalanced multi-class classification.

    Metrics tracked during training:
        - SparseCategoricalAccuracy

    Note:
        Precision, Recall and F1-score macro are computed
        after training with sklearn for reliability with
        sparse integer labels.

    Returns:
        List of Keras metrics.
    """

    return [
        tf.keras.metrics.SparseCategoricalAccuracy(
            name="accuracy"
        ),
    ]
