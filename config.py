"""
Project Configuration

This file contains all configurable paths and experiment
settings. It automatically detects whether the project is
running locally or on Google Colab.
"""

from pathlib import Path

# ==========================================================
# ENVIRONMENT
# ==========================================================

PROJECT_ROOT = Path(__file__).parent

COLAB_DATASET = Path(
    "/content/drive/MyDrive/spider_data/spider_data"
)

LOCAL_DATASET = PROJECT_ROOT / "data"

# Detect execution environment
if COLAB_DATASET.exists():
    DATA_ROOT = COLAB_DATASET
    ENVIRONMENT = "colab"
else:
    DATA_ROOT = LOCAL_DATASET
    ENVIRONMENT = "local"

# ==========================================================
# DATASET PATHS
# ==========================================================

DATABASE_ROOT = DATA_ROOT / "database"

DEV_JSON = DATA_ROOT / "dev.json"

TABLES_JSON = DATA_ROOT / "tables.json"

# ==========================================================
# PROMPTS
# ==========================================================

PROMPT_DIR = PROJECT_ROOT / "prompts"

DEFAULT_STRATEGY = "zero_shot"

DEFAULT_PROMPT_VERSION = "v2"

# ==========================================================
# MODEL
# ==========================================================

# ==========================================================
# MODEL
# ==========================================================

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"

LOAD_IN_4BIT = True

MAX_NEW_TOKENS = 256

TEMPERATURE = 0.0
# ==========================================================
# OUTPUT
# ==========================================================

if ENVIRONMENT == "colab":

    RESULTS_DIR = DATA_ROOT / "results"

else:

    RESULTS_DIR = PROJECT_ROOT / "results"

CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"

LOG_DIR = PROJECT_ROOT / "logs"

# ==========================================================
# RANDOM SEED
# ==========================================================

RANDOM_SEED = 42

# ==========================================================
# DEBUG
# ==========================================================

DEBUG = False