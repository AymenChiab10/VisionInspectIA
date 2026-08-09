"""
============================================================
Project : VisionInspectAI
File    : config.py
Author  : Aymen Chiab
Description:
    Global configuration file for the VisionInspectAI project.
    This file centralizes all project settings, paths,
    dataset parameters and training configuration.
============================================================
"""

from pathlib import Path


class Settings:
    """
    Global configuration class.
    """

    # ==========================================================
    # PROJECT INFORMATION
    # ==========================================================

    PROJECT_NAME = "VisionInspectAI"
    VERSION = "1.0.0"

    # ==========================================================
    # PROJECT ROOT
    # ==========================================================

    # VisionInspectIA/
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    # ==========================================================
    # DATA DIRECTORIES
    # ==========================================================

    DATA_PATH = PROJECT_ROOT / "data"

    RAW_DATA_PATH = DATA_PATH / "raw"
    PROCESSED_DATA_PATH = DATA_PATH / "processed"
    EXTERNAL_DATA_PATH = DATA_PATH / "external"

    # ==========================================================
    # DATASET
    # ==========================================================

    MVTEC_DATASET_PATH = RAW_DATA_PATH / "mvtec_anomaly_detection"

    BOTTLE_DATASET_PATH = MVTEC_DATASET_PATH / "bottle"

    # ==========================================================
    # AI DIRECTORIES
    # ==========================================================

    AI_PATH = PROJECT_ROOT / "ai"

    MODELS_PATH = AI_PATH / "models"

    SAVED_MODELS_PATH = AI_PATH / "saved_models"

    CHECKPOINTS_PATH = AI_PATH / "checkpoints"

    EXPERIMENTS_PATH = AI_PATH / "experiments"

    NOTEBOOKS_PATH = AI_PATH / "notebooks"

    # ==========================================================
    # RESULTS
    # ==========================================================

    RESULTS_PATH = AI_PATH / "results"

    FIGURES_PATH = RESULTS_PATH / "figures"

    REPORTS_PATH = RESULTS_PATH / "reports"

    LOGS_PATH = RESULTS_PATH / "logs"

    # ==========================================================
    # IMAGE PARAMETERS
    # ==========================================================

    IMAGE_WIDTH = 224

    IMAGE_HEIGHT = 224

    IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

    IMAGE_CHANNELS = 3

    # ==========================================================
    # DATASET CLASSES
    # ==========================================================

    CLASSES = [
    "broken_large",
    "broken_small",
    "contamination",
    "good",
    ]

    NUM_CLASSES = len(CLASSES)

    # ==========================================================
    # DATASET SPLIT
    # ==========================================================

    TRAIN_SPLIT = 0.50

    VALIDATION_SPLIT = 0.25

    TEST_SPLIT = 0.25

    RANDOM_SEED = 42

    # ==========================================================
    # FILES
    # ==========================================================

    ALLOWED_EXTENSIONS = [
        ".png",
        ".jpg",
        ".jpeg",
    ]

    # ==========================================================
    # TRAINING PARAMETERS
    # ==========================================================

    BATCH_SIZE = 32

    EPOCHS = 30

    LEARNING_RATE = 0.001

    SHUFFLE = True

    # ==========================================================
    # REPORT FILES
    # ==========================================================

    DATASET_REPORT = REPORTS_PATH / "dataset_report.json"

    TRAINING_REPORT = REPORTS_PATH / "training_report.json"

    # ==========================================================
    # FIGURES
    # ==========================================================

    CLASS_DISTRIBUTION_FIGURE = (
        FIGURES_PATH / "class_distribution.png"
    )

    IMAGE_SIZE_FIGURE = (
        FIGURES_PATH / "image_sizes.png"
    )

    # ==========================================================
    # LOG FILES
    # ==========================================================

    TRAINING_LOG = LOGS_PATH / "training.log"

    DATASET_LOG = LOGS_PATH / "dataset.log"

    AUGMENTED_DATA_PATH = DATA_PATH / "augmented"

    AUGMENTED_BOTTLE_PATH = AUGMENTED_DATA_PATH / "bottle"

    # ==========================================================
    # TARGET DATASET SIZE
    # ==========================================================

    TRAIN_IMAGES_PER_CLASS = 200

    VALIDATION_IMAGES_PER_CLASS = 40

    TEST_IMAGES_PER_CLASS = 40

    AUGMENTATION_SEED = 42

    # ==========================================================
    # TensorFlow Dataset
    # ==========================================================

    CACHE_DATASET = True

    PREFETCH_DATASET = True

    DATASET_SEED = 42

    USE_RAW_MVTEC_DATASET = False

    RAW_MVTEC_BOTTLE_PATH = MVTEC_DATASET_PATH / "bottle"

    USE_CLASS_WEIGHTS = True

    FINE_TUNE = False

    FINE_TUNE_LEARNING_RATE = 1e-5

    # ==========================================================
    # EXPERIMENTS
    # ==========================================================

    EXPERIMENT_MODE = "augmented_offline"

    EXPERIMENTS = {
        "raw_no_aug": {
            "name": "Raw MVTec - Feature Extraction sans augmentation",
            "dataset_type": "raw_mvtec",
            "augmentation": False,
            "description": "Baseline sur le dataset MVTec brut, sans augmentation.",
        },
        "raw_onfly": {
            "name": "Raw MVTec - Feature Extraction avec on-the-fly",
            "dataset_type": "raw_mvtec",
            "augmentation": True,
            "description": "Raw MVTec avec augmentation on-the-fly uniquement.",
        },
        "augmented_offline": {
            "name": "Dataset augmenté - Feature Extraction offline",
            "dataset_type": "augmented",
            "train_path": AUGMENTED_BOTTLE_PATH / "train",
            "validation_path": AUGMENTED_BOTTLE_PATH / "validation",
            "test_path": AUGMENTED_BOTTLE_PATH / "test",
            "augmentation": False,
            "description": "Dataset augmenté offline (train/validation/test).",
        },
    }

    # ==========================================================
    # LEGACY / COMPATIBILITY
    # ==========================================================

    USE_RAW_MVTEC_DATASET = EXPERIMENTS[EXPERIMENT_MODE]["dataset_type"] == "raw_mvtec"

    AUGMENTATION_TRAIN = EXPERIMENTS[EXPERIMENT_MODE].get("augmentation", False)

    SHARED_VALIDATION_PATH = AUGMENTED_BOTTLE_PATH / "validation"

    SHARED_TEST_PATH = AUGMENTED_BOTTLE_PATH / "test"

    # ==========================================================
    # MODEL
    # ==========================================================

    MODEL_TYPE = "resnet"

    MODEL_NAME = "resnet50"

    DROPOUT_RATE = 0.30

    PATIENCE = 5

    WEIGHT_DECAY = 1e-4

    LEARNING_RATE = 1e-3

    LABEL_SMOOTHING = 0.1

    TRAIN_STEPS_PER_EPOCH = 25

    # ==========================================================
    # ON-THE-FLY AUGMENTATION
    # ==========================================================

    AUGMENTATION_TRAIN = True

    RANDOM_FLIP_MODE = "horizontal"

    RANDOM_ROTATION_FACTOR = 0.1

    RANDOM_ZOOM_HEIGHT = (-0.1, 0.1)

    RANDOM_ZOOM_WIDTH = (-0.1, 0.1)

    RANDOM_TRANSLATION_HEIGHT = 0.1

    RANDOM_TRANSLATION_WIDTH = 0.1

    RANDOM_CONTRAST_FACTOR = 0.1

    # ==========================================================
    # CALLBACKS
    # ==========================================================

    CHECKPOINT_MONITOR = "val_loss"

    CHECKPOINT_MODE = "min"

    SAVE_BEST_ONLY = True

    EARLY_STOPPING_PATIENCE = 8

    REDUCE_LR_PATIENCE = 4

    REDUCE_LR_FACTOR = 0.2

    MIN_LEARNING_RATE = 1e-6

    TENSORBOARD_LOG_DIR = LOGS_PATH / "tensorboard"

    CSV_LOGGER_FILE = LOGS_PATH / "training.csv"

    @classmethod
    def create_directories(cls):
        """
        Create all required directories if they do not exist.
        """

        directories = [
            cls.RAW_DATA_PATH,
            cls.PROCESSED_DATA_PATH,
            cls.EXTERNAL_DATA_PATH,
            cls.MODELS_PATH,
            cls.SAVED_MODELS_PATH,
            cls.CHECKPOINTS_PATH,
            cls.EXPERIMENTS_PATH,
            cls.RESULTS_PATH,
            cls.FIGURES_PATH,
            cls.REPORTS_PATH,
            cls.LOGS_PATH,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    # ==========================================================
    # DISPLAY CONFIGURATION
    # ==========================================================

    @classmethod
    def show(cls):
        """
        Display project configuration.
        """

        print("=" * 60)
        print(f"Project        : {cls.PROJECT_NAME}")
        print(f"Version        : {cls.VERSION}")
        print(f"Project Root   : {cls.PROJECT_ROOT}")
        print(f"Dataset Path   : {cls.BOTTLE_DATASET_PATH}")
        print(f"Image Size     : {cls.IMAGE_SIZE}")
        print(f"Classes        : {cls.CLASSES}")
        print(f"Batch Size     : {cls.BATCH_SIZE}")
        print(f"Epochs         : {cls.EPOCHS}")
        print("=" * 60)


# ==============================================================
# Initialize configuration
# ==============================================================

settings = Settings()

Settings.create_directories()


# ==============================================================
# Debug
# ==============================================================

if __name__ == "__main__":
    Settings.show()