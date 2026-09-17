import json
from pathlib import Path


RESULTS_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results/reconciled"
)

FILES = {
    "Qwen_ZeroShot": "Qwen_ZeroShot_reconciled.jsonl",
    "Qwen_Pruning": "Qwen_Pruning_reconciled.jsonl",
    "Qwen_Hybrid": "Qwen_Hybrid_reconciled.jsonl",
    "DeepSeek_ZeroShot": "DeepSeek_ZeroShot_reconciled.jsonl",
    "DeepSeek_Hybrid": "DeepSeek_Hybrid_reconciled.jsonl",
    "Llama_ZeroShot": "Llama_ZeroShot_reconciled.jsonl",
    "Llama_Hybrid": "Llama_Hybrid_reconciled.jsonl",
}


for experiment, filename in FILES.items():

    path = RESULTS_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        first_row = json.loads(next(f))

    print("\n" + "=" * 80)
    print(experiment)
    print("=" * 80)

    print("Available fields:")

    for key in first_row.keys():
        print(f"  {key}")