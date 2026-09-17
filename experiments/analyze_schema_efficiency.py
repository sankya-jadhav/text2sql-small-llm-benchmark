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
        rows = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    avg_full_columns = sum(
        r["full_schema_columns"]
        for r in rows
    ) / len(rows)

    avg_pruned_columns = sum(
        r["pruned_schema_columns"]
        for r in rows
    ) / len(rows)

    avg_reduction = sum(
        r["schema_reduction_percent"]
        for r in rows
    ) / len(rows)

    avg_prompt_tokens = sum(
        r.get("prompt_tokens", 0) or 0
        for r in rows
    ) / len(rows)

    avg_completion_tokens = sum(
        r.get("completion_tokens", 0) or 0
        for r in rows
    ) / len(rows)

    avg_total_tokens = sum(
        r.get("total_tokens", 0) or 0
        for r in rows
    ) / len(rows)

    print("\n" + "=" * 90)
    print(experiment)
    print("=" * 90)

    print(
        f"Full schema columns:    {avg_full_columns:.2f}"
    )

    print(
        f"Working schema columns: {avg_pruned_columns:.2f}"
    )

    print(
        f"Schema reduction:       {avg_reduction:.2f}%"
    )

    print(
        f"Prompt tokens:           {avg_prompt_tokens:.2f}"
    )

    print(
        f"Completion tokens:      {avg_completion_tokens:.2f}"
    )

    print(
        f"Total tokens:            {avg_total_tokens:.2f}"
    )


# ------------------------------------------------------------
# Direct model-level pruning comparison
# ------------------------------------------------------------

print("\n")
print("=" * 90)
print("MODEL-LEVEL ZERO-SHOT → PRUNING TOKEN REDUCTION")
print("=" * 90)

pairs = [
    (
        "Qwen",
        "Qwen_ZeroShot_reconciled.jsonl",
        "Qwen_Pruning_reconciled.jsonl",
    ),
    (
        "DeepSeek",
        "DeepSeek_ZeroShot_reconciled.jsonl",
        "DeepSeek_Hybrid_reconciled.jsonl",
    ),
    (
        "Llama",
        "Llama_ZeroShot_reconciled.jsonl",
        "Llama_Hybrid_reconciled.jsonl",
    ),
]

for model, baseline_file, pruned_file in pairs:

    with open(
        RESULTS_DIR / baseline_file,
        "r",
        encoding="utf-8"
    ) as f:
        baseline = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    with open(
        RESULTS_DIR / pruned_file,
        "r",
        encoding="utf-8"
    ) as f:
        pruned = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    baseline_prompt = sum(
        r["prompt_tokens"]
        for r in baseline
    ) / len(baseline)

    pruned_prompt = sum(
        r["prompt_tokens"]
        for r in pruned
    ) / len(pruned)

    reduction = (
        (baseline_prompt - pruned_prompt)
        / baseline_prompt
        * 100
    )

    print(
        f"{model:<12}"
        f"{baseline_prompt:>10.2f} → "
        f"{pruned_prompt:<10.2f}"
        f" Reduction: {reduction:>6.2f}%"
    )