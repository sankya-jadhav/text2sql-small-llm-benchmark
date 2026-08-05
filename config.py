# ==========================================================
# DATASET
# ==========================================================

from pathlib import Path

COLAB_DATASET = Path("/content/drive/MyDrive/spider_data/spider_data")

if COLAB_DATASET.exists():
    DATA_ROOT = COLAB_DATASET
else:
    DATA_ROOT = Path("data")

DATABASE_ROOT = DATA_ROOT / "database"
DEV_JSON = DATA_ROOT / "dev.json"
TABLES_JSON = DATA_ROOT / "tables.json"
# ==========================================================
# MODEL
# ==========================================================

MODEL_NAME = "qwen2.5-coder:7b"

TEMPERATURE = 0.0

MAX_TOKENS = 256

# ==========================================================
# EXPERIMENT
# ==========================================================

DEFAULT_PROMPT = "zero-shot"

# ==========================================================
# OUTPUT
# ==========================================================

RESULTS_DIR = "results"

CHECKPOINT_DIR = "checkpoints"

LOG_DIR = "logs"