"""
============================================================
Project : VisionInspectAI
File    : trainer.py
Author  : Aymen Chiab

Description:
    Generic TensorFlow model trainer.
============================================================
"""

from __future__ import annotations

import json
import logging
import sys

from datetime import datetime

import numpy as np
import tensorflow as tf

from ai.config.config import settings
from ai.training.callbacks import TrainingCallbacks


class Trainer:
    """
    Generic TensorFlow trainer.
    """

    def __init__(
        self,
        model: tf.keras.Model,
        train_dataset: tf.data.Dataset,
        validation_dataset: tf.data.Dataset,
        test_dataset: tf.data.Dataset,
        architecture_name: str | None = None,
    ) -> None:

        self.model = model

        self.train_dataset = train_dataset

        self.validation_dataset = validation_dataset

        self.test_dataset = test_dataset

        self.architecture_name = architecture_name or settings.MODEL_NAME

        self.history = None

        self.logger = self.setup_logger()

        self.callbacks = TrainingCallbacks().get_callbacks()

        self.training_time = None

        self.evaluation_time = None

        self.inference_time = None

        self.model_size_mb = None

        self.logger.info("Trainer initialized.")

    # =====================================================
    # LOGGER
    # =====================================================

    def setup_logger(self) -> logging.Logger:
        """
        Configure trainer logger.
        """

        logger = logging.getLogger("Trainer")

        logger.setLevel(logging.INFO)

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            settings.LOGS_PATH / "trainer.log",
            encoding="utf-8",
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

    def print_header(self) -> None:
        """
        Print pipeline header.
        """

        print()

        print("=" * 60)

        print("VisionInspectAI")

        print("Model Training")

        print("=" * 60)

        print()

        print(f"Model : {self.model.name}")

        print()

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(self) -> None:
        """
        Validate inputs before training.
        """

        if self.model is None:
            raise ValueError("Model is None.")

        if self.train_dataset is None:
            raise ValueError("Training dataset is missing.")

        if self.validation_dataset is None:
            raise ValueError("Validation dataset is missing.")

        if self.test_dataset is None:
            raise ValueError("Test dataset is missing.")

        self.logger.info("Trainer validated.")

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    def display_dataset_statistics(self) -> None:
        """
        Display dataset statistics: images, batches, classes.
        """

        print()

        print("=" * 60)

        print("Dataset Information")

        print("=" * 60)

        print()

        train_batches = int(
            tf.data.experimental.cardinality(self.train_dataset).numpy()
        )

        validation_batches = int(
            tf.data.experimental.cardinality(self.validation_dataset).numpy()
        )

        test_batches = int(
            tf.data.experimental.cardinality(self.test_dataset).numpy()
        )

        train_images = train_batches * settings.BATCH_SIZE

        validation_images = validation_batches * settings.BATCH_SIZE

        test_images = test_batches * settings.BATCH_SIZE

        total_images = train_images + validation_images + test_images

        print(f"Train Images      : {train_images}")

        print(f"Validation Images : {validation_images}")

        print(f"Test Images       : {test_images}")

        print(f"Total Images      : {total_images}")

        print()

        print(f"Train Batches     : {train_batches}")

        print(f"Validation Batches: {validation_batches}")

        print(f"Test Batches      : {test_batches}")

        print()

        print(f"Classes           : {settings.NUM_CLASSES}")

        print(f"Class Names       : {settings.CLASSES}")

        print()

    # =====================================================
    # MODEL INFORMATION
    # =====================================================

    def display_model_summary(self) -> None:
        """
        Display model architecture and parameters.
        """

        print()

        print("=" * 60)

        print("Model Information")

        print("=" * 60)

        print()

        print(f"Model Name        : {self.model.name}")

        print(f"Input Shape       : {self.model.input_shape}")

        print(f"Output Shape      : {self.model.output_shape}")

        print()

        trainable_params = self.model.count_params()

        print(f"Total Parameters  : {trainable_params:,}")

        print()

        optimizer = self.model.optimizer

        if optimizer is not None:
            print(f"Optimizer         : {optimizer.__class__.__name__}")

            print(f"Learning Rate     : {optimizer.learning_rate.numpy():.6f}")

        else:
            print("Optimizer         : Not compiled")

        loss_fn = self.model.compiled_loss

        if loss_fn is not None:
            print(f"Loss              : {loss_fn.__class__.__name__}")

        else:
            print("Loss              : Not compiled")

        print(f"Dropout Rate      : {settings.DROPOUT_RATE}")

        print(f"Weight Decay      : {settings.WEIGHT_DECAY}")

        print()

    # =====================================================
    # TRAINING CONFIGURATION
    # =====================================================

    def display_training_config(self) -> None:
        """
        Display training configuration.
        """

        print()

        print("=" * 60)

        print("Training Configuration")

        print("=" * 60)

        print()

        print(f"Epochs            : {settings.EPOCHS}")

        print(f"Batch Size        : {settings.BATCH_SIZE}")

        print(f"Learning Rate     : {settings.LEARNING_RATE}")

        print(f"Patience          : {settings.PATIENCE}")

        print(f"Checkpoint Monitor: {settings.CHECKPOINT_MONITOR}")

        print(f"Early Stopping    : {settings.EARLY_STOPPING_PATIENCE}")

        print(f"Reduce LR Factor  : {settings.REDUCE_LR_FACTOR}")

        print(f"Min Learning Rate : {settings.MIN_LEARNING_RATE}")

        print()

    # =====================================================
    # PREPROCESSING VERIFICATION
    # =====================================================

    def verify_preprocessing(self) -> None:
        """
        Verify that preprocessing is correctly applied.

        Takes one batch from the training dataset and passes it
        through the first preprocessing layer of the model to
        verify the expected input/output ranges.
        """

        print()

        print("=" * 60)

        print("Preprocessing Verification")

        print("=" * 60)

        print()

        images, _ = next(iter(self.train_dataset))

        print(f"Input dtype  : {images.dtype}")
        print(f"Input shape  : {images.shape}")
        print(f"Input min    : {tf.reduce_min(images).numpy():.3f}")
        print(f"Input max    : {tf.reduce_max(images).numpy():.3f}")

        print()

        preprocessed = self.model.layers[1](images)

        print(f"Output dtype : {preprocessed.dtype}")
        print(f"Output shape : {preprocessed.shape}")
        print(f"Output min   : {tf.reduce_min(preprocessed).numpy():.3f}")
        print(f"Output max   : {tf.reduce_max(preprocessed).numpy():.3f}")

        print()

    # =====================================================
    # CLASS WEIGHTS
    # =====================================================

    def compute_class_weights(self) -> dict[int, float] | None:
        """
        Compute class weights from training dataset labels.
        """

        if not settings.USE_CLASS_WEIGHTS:

            self.logger.info("Class weights disabled.")

            return None

        labels = []

        for _, batch_labels in self.train_dataset:

            labels.extend(
                batch_labels.numpy().flatten().tolist()
            )

        labels = np.array(labels)

        classes = np.unique(labels)

        weights = {}

        total = len(labels)

        for cls in classes:

            count = np.sum(labels == cls)

            weight = total / (len(classes) * count)

            weights[int(cls)] = float(weight)

        self.logger.info(f"Class weights: {weights}")

        return weights
        # =====================================================
    # TRAIN
    # =====================================================

    def train(self) -> tf.keras.callbacks.History:
        """
        Train the TensorFlow model.
        """

        self.logger.info("Starting training...")

        start_time = datetime.now()

        class_weight = self.compute_class_weights()

        self.history = self.model.fit(
            self.train_dataset,
            validation_data=self.validation_dataset,
            epochs=settings.EPOCHS,
            callbacks=self.callbacks,
            class_weight=class_weight,
            verbose=1,
        )

        self.training_time = datetime.now() - start_time

        self.logger.info(
            f"Training completed in {self.training_time}."
        )

        return self.history

    # =====================================================
    # SAVE HISTORY
    # =====================================================

    def save_history(self) -> None:
        """
        Save training history to JSON and CSV.
        """

        if self.history is None:
            raise ValueError("No training history available.")

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        history_file = model_dir / "history.json"

        with open(history_file, "w", encoding="utf-8") as file:
            json.dump(self.history.history, file, indent=4)

        self.logger.info("Training history saved.")

    # =====================================================
    # SAVE MODEL
    # =====================================================

    def save_model(self) -> None:
        """
        Save the trained model.
        """

        model_dir = settings.SAVED_MODELS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        output = model_dir / "best_model.keras"

        self.model.save(output)

        self.logger.info(f"Model saved successfully: {output}")

    # =====================================================
    # EVALUATE
    # =====================================================

    def evaluate(self) -> list[float]:
        """
        Evaluate trained model on test dataset.
        """

        self.logger.info("Evaluating model...")

        start_time = datetime.now()

        results = self.model.evaluate(self.test_dataset, verbose=1)

        self.evaluation_time = datetime.now() - start_time

        print()

        print("=" * 60)

        print("Test Results")

        print("=" * 60)

        print()

        for metric, value in zip(self.model.metrics_names, results):
            print(f"{metric:<15}: {value:.4f}")

        print()

        print(f"Evaluation Time : {self.evaluation_time}")

        print()

        self.logger.info("Model evaluation completed.")

        return results

    # =====================================================
    # EXPORT METRICS
    # =====================================================

    def export_metrics(self, results: list[float]) -> None:
        """
        Export evaluation metrics to JSON.
        """

        metrics = {}

        for name, value in zip(self.model.metrics_names, results):
            metrics[name] = float(value)

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        output = model_dir / "metrics.json"

        with open(output, "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4)

        self.logger.info("Metrics exported.")

    # =====================================================
    # CONFUSION MATRIX
    # =====================================================

    def compute_confusion_matrix(self) -> None:
        """
        Compute and save confusion matrix.
        """

        import numpy as np
        from sklearn.metrics import confusion_matrix

        print()

        print("=" * 60)

        print("Confusion Matrix")

        print("=" * 60)

        print()

        y_true = []

        y_pred = []

        for images, labels in self.test_dataset:
            predictions = self.model.predict(images, verbose=0)

            y_pred.extend(np.argmax(predictions, axis=1))

            y_true.extend(labels.numpy())

        cm = confusion_matrix(y_true, y_pred)

        print(cm)

        print()

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        np.save(model_dir / "confusion_matrix.npy", cm)

        self.logger.info("Confusion matrix computed and saved.")

        return cm

    # =====================================================
    # CLASSIFICATION REPORT
    # =====================================================

    def compute_classification_report(self) -> dict:
        """
        Compute classification report.
        """

        import numpy as np
        from sklearn.metrics import classification_report

        print()

        print("=" * 60)

        print("Classification Report")

        print("=" * 60)

        print()

        y_true = []

        y_pred = []

        for images, labels in self.test_dataset:
            predictions = self.model.predict(images, verbose=0)

            y_pred.extend(np.argmax(predictions, axis=1))

            y_true.extend(labels.numpy())

        report = classification_report(
            y_true,
            y_pred,
            labels=list(range(settings.NUM_CLASSES)),
            target_names=settings.CLASSES,
            output_dict=True,
        )

        print(classification_report(
            y_true,
            y_pred,
            labels=list(range(settings.NUM_CLASSES)),
            target_names=settings.CLASSES
        ))

        print()

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        with open(model_dir / "classification_report.json", "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        self.logger.info("Classification report saved.")

        return report

    # =====================================================
    # SKLEARN METRICS
    # =====================================================

    def compute_sklearn_metrics(self) -> dict:
        """
        Compute macro-averaged Precision, Recall and F1-score
        using sklearn for reliable imbalanced evaluation.
        """

        import numpy as np
        from sklearn.metrics import (
            f1_score,
            precision_score,
            recall_score,
        )

        print()

        print("=" * 60)

        print("Macro Metrics (sklearn)")

        print("=" * 60)

        print()

        y_true = []

        y_pred = []

        for images, labels in self.test_dataset:

            predictions = self.model.predict(images, verbose=0)

            y_pred.extend(np.argmax(predictions, axis=1))

            y_true.extend(labels.numpy())

        y_true = np.array(y_true)

        y_pred = np.array(y_pred)

        precision_macro = float(
            precision_score(y_true, y_pred, average="macro", zero_division=0)
        )

        recall_macro = float(
            recall_score(y_true, y_pred, average="macro", zero_division=0)
        )

        f1_macro = float(
            f1_score(y_true, y_pred, average="macro", zero_division=0)
        )

        metrics = {
            "precision_macro": precision_macro,
            "recall_macro": recall_macro,
            "f1_score_macro_sklearn": f1_macro,
        }

        for key, value in metrics.items():

            print(f"{key:<25}: {value:.4f}")

        print()

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        with open(model_dir / "sklearn_metrics.json", "w", encoding="utf-8") as file:

            json.dump(metrics, file, indent=4)

        self.logger.info("Sklearn metrics computed and saved.")

        return metrics

    # =====================================================
    # INFERENCE TIME
    # =====================================================

    def compute_inference_time(self, num_samples: int = 100) -> float:
        """
        Measure average inference time per image.

        Args:
            num_samples: Number of samples to use for timing.

        Returns:
            Average inference time in milliseconds.
        """

        import time

        samples_used = 0

        total_time = 0.0

        for images, _ in self.test_dataset:

            batch_size = images.shape[0]

            start_time = time.perf_counter()

            _ = self.model.predict(images, verbose=0)

            end_time = time.perf_counter()

            total_time += end_time - start_time

            samples_used += batch_size

            if samples_used >= num_samples:
                break

        avg_time_ms = (total_time / samples_used) * 1000

        self.inference_time = avg_time_ms

        print()

        print(f"Inference Time (avg) : {avg_time_ms:.2f} ms/image")

        print()

        self.logger.info(
            f"Inference time: {avg_time_ms:.2f} ms/image "
            f"({samples_used} samples)"
        )

        return avg_time_ms

    # =====================================================
    # MODEL SIZE
    # =====================================================

    def compute_model_size(self) -> float:
        """
        Compute saved model size in megabytes.

        Returns:
            Model size in MB.
        """

        model_path = settings.SAVED_MODELS_PATH / settings.MODEL_NAME / "best_model.keras"

        size_bytes = model_path.stat().st_size

        size_mb = size_bytes / (1024 * 1024)

        self.model_size_mb = size_mb

        print()

        print(f"Model Size          : {size_mb:.2f} MB")

        print()

        self.logger.info(f"Model size: {size_mb:.2f} MB")

        return size_mb

    # =====================================================
    # BENCHMARK RESULTS
    # =====================================================

    def update_benchmark_results(self, report: dict, sklearn_metrics: dict) -> None:
        """
        Update central benchmark results file.

        Args:
            report: Training report dictionary.
            sklearn_metrics: Sklearn metrics dictionary.
        """

        benchmark_path = settings.RESULTS_PATH / "benchmark_results.json"

        benchmark_path.parent.mkdir(parents=True, exist_ok=True)

        if benchmark_path.exists():

            with open(benchmark_path, "r", encoding="utf-8") as file:

                benchmark_data = json.load(file)

        else:

            benchmark_data = {
                "benchmark_date": str(datetime.now()),
                "dataset": "raw MVTec Bottle",
                "reproducibility": {
                    "tensorflow_version": tf.__version__,
                    "python_version": sys.version.split()[0],
                    "random_seed": settings.RANDOM_SEED,
                    "dataset_seed": settings.DATASET_SEED,
                    "augmentation_seed": settings.AUGMENTATION_SEED,
                    "epochs": settings.EPOCHS,
                    "batch_size": settings.BATCH_SIZE,
                    "learning_rate": settings.LEARNING_RATE,
                    "optimizer": "AdamW",
                    "loss": "SparseCategoricalCrossentropy",
                    "dropout": settings.DROPOUT_RATE,
                    "weight_decay": settings.WEIGHT_DECAY,
                    "image_size": list(settings.IMAGE_SIZE),
                    "num_classes": settings.NUM_CLASSES,
                    "classes": settings.CLASSES,
                },
                "models": [],
            }

        model_entry = {
            "model_name": settings.MODEL_NAME,
            "architecture": self.architecture_name,
            "total_parameters": int(self.model.count_params()),
            "model_size_mb": self.model_size_mb,
            "training_time": str(self.training_time),
            "inference_time_ms": self.inference_time,
            "accuracy": float(report["final_accuracy"]),
            "precision_macro": sklearn_metrics.get("precision_macro"),
            "recall_macro": sklearn_metrics.get("recall_macro"),
            "f1_score_macro": sklearn_metrics.get("f1_score_macro_sklearn"),
            "best_epoch": report["best_epoch"],
            "best_val_accuracy": report["best_validation_accuracy"],
            "best_val_loss": report["best_validation_loss"],
            "model_path": str(
                settings.SAVED_MODELS_PATH / settings.MODEL_NAME / "best_model.keras"
            ),
            "results_path": str(settings.RESULTS_PATH / settings.MODEL_NAME),
            "reproducibility": {
                "tensorflow_version": tf.__version__,
                "python_version": sys.version.split()[0],
                "random_seed": settings.RANDOM_SEED,
                "dataset_seed": settings.DATASET_SEED,
                "augmentation_seed": settings.AUGMENTATION_SEED,
                "epochs": settings.EPOCHS,
                "batch_size": settings.BATCH_SIZE,
                "learning_rate": settings.LEARNING_RATE,
                "optimizer": self.model.optimizer.__class__.__name__,
                "loss": self.model.compiled_loss.__class__.__name__,
                "dropout": settings.DROPOUT_RATE,
                "weight_decay": settings.WEIGHT_DECAY,
                "image_size": list(settings.IMAGE_SIZE),
                "num_classes": settings.NUM_CLASSES,
                "classes": settings.CLASSES,
            },
            "configuration": report["configuration"],
            "dataset": report["dataset"],
        }

        existing_index = None

        for index, entry in enumerate(benchmark_data["models"]):

            if entry["model_name"] == settings.MODEL_NAME:
                existing_index = index
                break

        if existing_index is not None:
            benchmark_data["models"][existing_index] = model_entry
        else:
            benchmark_data["models"].append(model_entry)

        benchmark_data["last_updated"] = str(datetime.now())

        with open(benchmark_path, "w", encoding="utf-8") as file:

            json.dump(benchmark_data, file, indent=4)

        print()

        print(f"Benchmark updated   : {benchmark_path}")

        print()

        self.logger.info(
            f"Benchmark results updated for {settings.MODEL_NAME}"
        )

    # =====================================================
    # TRAINING CURVES
    # =====================================================

    def plot_training_curves(self) -> None:
        """
        Plot accuracy and loss curves.
        """

        import matplotlib.pyplot as plt

        if self.history is None:
            raise ValueError("No training history available.")

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        history = self.history.history

        epochs = range(1, len(history["accuracy"]) + 1)

        # Accuracy

        plt.figure(figsize=(10, 5))

        plt.plot(epochs, history["accuracy"], label="Train Accuracy")

        plt.plot(epochs, history["val_accuracy"], label="Validation Accuracy")

        plt.title("Model Accuracy")

        plt.xlabel("Epoch")

        plt.ylabel("Accuracy")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(model_dir / "accuracy.png", dpi=300)

        plt.close()

        # Loss

        plt.figure(figsize=(10, 5))

        plt.plot(epochs, history["loss"], label="Train Loss")

        plt.plot(epochs, history["val_loss"], label="Validation Loss")

        plt.title("Model Loss")

        plt.xlabel("Epoch")

        plt.ylabel("Loss")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(model_dir / "loss.png", dpi=300)

        plt.close()

        self.logger.info("Training curves saved.")

    # =====================================================
    # FINAL REPORT
    # =====================================================

    def generate_training_report(
        self,
        results: list[float],
        sklearn_metrics: dict | None = None,
    ) -> dict:
        """
        Generate final training report.
        """

        if self.history is None:
            raise ValueError("No training history available.")

        history = self.history.history

        best_epoch = int(np.argmin(history["val_loss"])) + 1

        best_val_loss = float(min(history["val_loss"]))

        best_val_accuracy = float(max(history["val_accuracy"]))

        final_loss = float(history["loss"][-1])

        final_accuracy = float(history["accuracy"][-1])

        report = {
            "date": str(datetime.now()),
            "model_name": settings.MODEL_NAME,
            "training_time": str(self.training_time),
            "evaluation_time": str(self.evaluation_time),
            "inference_time_ms": self.inference_time,
            "model_size_mb": self.model_size_mb,
            "final_loss": final_loss,
            "final_accuracy": final_accuracy,
            "best_epoch": best_epoch,
            "best_validation_loss": best_val_loss,
            "best_validation_accuracy": best_val_accuracy,
            "total_parameters": int(self.model.count_params()),
            "configuration": {
                "epochs": settings.EPOCHS,
                "batch_size": settings.BATCH_SIZE,
                "learning_rate": settings.LEARNING_RATE,
                "optimizer": self.model.optimizer.__class__.__name__,
                "loss": self.model.compiled_loss.__class__.__name__,
                "dropout": settings.DROPOUT_RATE,
                "weight_decay": settings.WEIGHT_DECAY,
                "image_size": list(settings.IMAGE_SIZE),
                "num_classes": settings.NUM_CLASSES,
            },
            "dataset": {
                "train_images": int(
                    tf.data.experimental.cardinality(self.train_dataset).numpy()
                )
                * settings.BATCH_SIZE,
                "validation_images": int(
                    tf.data.experimental.cardinality(self.validation_dataset).numpy()
                )
                * settings.BATCH_SIZE,
                "test_images": int(
                    tf.data.experimental.cardinality(self.test_dataset).numpy()
                )
                * settings.BATCH_SIZE,
                "classes": settings.CLASSES,
            },
            "test_metrics": {},
            "sklearn_metrics": sklearn_metrics or {},
        }

        for name, value in zip(self.model.metrics_names, results):
            report["test_metrics"][name] = float(value)

        model_dir = settings.RESULTS_PATH / settings.MODEL_NAME

        model_dir.mkdir(parents=True, exist_ok=True)

        output = model_dir / "training_report.json"

        with open(output, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        self.logger.info("Training report generated.")

        return report

    # =====================================================
    # RUN
    # =====================================================

    def run(self) -> None:
        """
        Execute complete training pipeline.
        """

        self.print_header()

        self.validate()

        self.display_dataset_statistics()

        self.display_model_summary()

        self.verify_preprocessing()

        self.display_training_config()

        self.train()

        self.save_history()

        self.save_model()

        results = self.evaluate()

        self.export_metrics(results)

        self.compute_confusion_matrix()

        self.compute_classification_report()

        sklearn_metrics = self.compute_sklearn_metrics()

        self.compute_inference_time()

        self.compute_model_size()

        self.plot_training_curves()

        report = self.generate_training_report(results, sklearn_metrics)

        self.update_benchmark_results(report, sklearn_metrics)

        print()

        print("=" * 60)

        print("Training Pipeline Completed")

        print("=" * 60)

        print()

        print(f"Training Time     : {self.training_time}")

        print(f"Best Epoch        : {report['best_epoch']}")

        print(f"Best Val Accuracy : {report['best_validation_accuracy']:.4f}")

        print(f"Best Val Loss     : {report['best_validation_loss']:.4f}")

        print(f"Final Accuracy    : {report['final_accuracy']:.4f}")

        print(f"Final Loss        : {report['final_loss']:.4f}")

        print(f"Inference Time    : {self.inference_time:.2f} ms/image")

        print(f"Model Size        : {self.model_size_mb:.2f} MB")

        print()

        print(f"Model saved to    : {settings.SAVED_MODELS_PATH / settings.MODEL_NAME}")

        print(f"Results saved to  : {settings.RESULTS_PATH / settings.MODEL_NAME}")

        print()

        self.logger.info("Training pipeline completed.")


# =====================================================
# MAIN
# =====================================================

def main() -> None:
    print()

    print("=" * 60)

    print("Trainer module")

    print("=" * 60)

    print()

    print("This module is intended to be used")

    print("from train.py")

    print()


if __name__ == "__main__":
    main()
