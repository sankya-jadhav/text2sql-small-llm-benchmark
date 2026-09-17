import json
from pathlib import Path


RESULTS_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results/reconciled"
)

ORIGINAL_RESULTS_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results"
)


FILES = {
    "Qwen_ZeroShot": (
        ORIGINAL_RESULTS_DIR
        / "Qwen2.5-Coder-7B-Instruct"
        / "zero_shot_v2.jsonl"
    ),

    "Qwen_Pruning": (
        RESULTS_DIR
        / "Qwen_Pruning_reconciled.jsonl"
    ),

    "Qwen_Hybrid": (
        RESULTS_DIR
        / "Qwen_Hybrid_reconciled.jsonl"
    ),

    "DeepSeek_ZeroShot": (
        RESULTS_DIR
        / "DeepSeek_ZeroShot_reconciled.jsonl"
    ),

    "DeepSeek_Hybrid": (
        RESULTS_DIR
        / "DeepSeek_Hybrid_reconciled.jsonl"
    ),

    "Llama_ZeroShot": (
        RESULTS_DIR
        / "Llama_ZeroShot_reconciled.jsonl"
    ),

    "Llama_Hybrid": (
        RESULTS_DIR
        / "Llama_Hybrid_reconciled.jsonl"
    ),
}


def load_jsonl(path):

    with open(path, "r", encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


print("=" * 100)
print("SCHEMA AND TOKEN EFFICIENCY")
print("=" * 100)


for experiment, path in FILES.items():

    rows = load_jsonl(path)

    if len(rows) != 180:
        raise ValueError(
            f"{experiment}: expected 180 rows, "
            f"found {len(rows)}"
        )

    required_fields = [
        "full_schema_columns",
        "pruned_schema_columns",
        "schema_reduction_percent",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
    ]

    missing = [
        field
        for field in required_fields
        if field not in rows[0]
    ]

    if missing:

        raise ValueError(
            f"{experiment} is missing fields: {missing}"
        )

    avg_full_columns = sum(
        r["full_schema_columns"]
        for r in rows
    ) / len(rows)

    avg_working_columns = sum(
        r["pruned_schema_columns"]
        for r in rows
    ) / len(rows)

    avg_reduction = sum(
        r["schema_reduction_percent"]
        for r in rows
    ) / len(rows)

    avg_prompt_tokens = sum(
        r["prompt_tokens"]
        for r in rows
    ) / len(rows)

    avg_completion_tokens = sum(
        r["completion_tokens"]
        for r in rows
    ) / len(rows)

    avg_total_tokens = sum(
        r["total_tokens"]
        for r in rows
    ) / len(rows)

    print("\n" + "-" * 100)
    print(experiment)
    print("-" * 100)

    print(
        f"Full schema columns:    "
        f"{avg_full_columns:.2f}"
    )

    print(
        f"Working schema columns: "
        f"{avg_working_columns:.2f}"
    )

    print(
        f"Schema reduction:       "
        f"{avg_reduction:.2f}%"
    )

    print(
        f"Prompt tokens:           "
        f"{avg_prompt_tokens:.2f}"
    )

    print(
        f"Completion tokens:      "
        f"{avg_completion_tokens:.2f}"
    )

    print(
        f"Total tokens:            "
        f"{avg_total_tokens:.2f}"
    )


# ============================================================
# TRUE STANDALONE PRUNING COMPARISON
# ============================================================

print("\n")
print("=" * 100)
print("QWEN: ZERO-SHOT → STANDALONE PRUNING")
print("=" * 100)


qwen_zero = load_jsonl(
    FILES["Qwen_ZeroShot"]
)

qwen_pruning = load_jsonl(
    FILES["Qwen_Pruning"]
)


zero_prompt = sum(
    r["prompt_tokens"]
    for r in qwen_zero
) / len(qwen_zero)

pruning_prompt = sum(
    r["prompt_tokens"]
    for r in qwen_pruning
) / len(qwen_pruning)

prompt_reduction = (
    (zero_prompt - pruning_prompt)
    / zero_prompt
    * 100
)


zero_total = sum(
    r["total_tokens"]
    for r in qwen_zero
) / len(qwen_zero)

pruning_total = sum(
    r["total_tokens"]
    for r in qwen_pruning
) / len(qwen_pruning)

total_reduction = (
    (zero_total - pruning_total)
    / zero_total
    * 100
)


zero_columns = sum(
    r["full_schema_columns"]
    for r in qwen_zero
) / len(qwen_zero)

pruning_columns = sum(
    r["pruned_schema_columns"]
    for r in qwen_pruning
) / len(qwen_pruning)

schema_reduction = (
    (zero_columns - pruning_columns)
    / zero_columns
    * 100
)


print(
    f"Average schema columns: "
    f"{zero_columns:.2f} → "
    f"{pruning_columns:.2f}"
)

print(
    f"Schema reduction: "
    f"{schema_reduction:.2f}%"
)

print(
    f"Average prompt tokens: "
    f"{zero_prompt:.2f} → "
    f"{pruning_prompt:.2f}"
)

print(
    f"Prompt-token reduction: "
    f"{prompt_reduction:.2f}%"
)

print(
    f"Average total tokens: "
    f"{zero_total:.2f} → "
    f"{pruning_total:.2f}"
)

print(
    f"Total-token reduction: "
    f"{total_reduction:.2f}%"
)


# ============================================================
# MODEL-LEVEL PRUNED-SCHEMA TOKEN COMPARISON
#
# NOTE:
# DeepSeek and Llama Hybrid use the pruned schema, but these
# are NOT standalone pruning experiments. We therefore report
# these as Hybrid vs Zero-shot context differences rather than
# as independent pruning effects.
# ============================================================

print("\n")
print("=" * 100)
print("PRUNED-SCHEMA CONTEXT COMPARISON")
print("=" * 100)


pairs = [
    (
        "DeepSeek",
        "DeepSeek_ZeroShot",
        "DeepSeek_Hybrid",
    ),

    (
        "Llama",
        "Llama_ZeroShot",
        "Llama_Hybrid",
    ),
]


for model, baseline_name, pruned_name in pairs:

    baseline = load_jsonl(
        FILES[baseline_name]
    )

    pruned = load_jsonl(
        FILES[pruned_name]
    )

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
        f"{baseline_prompt:.2f} → "
        f"{pruned_prompt:.2f} "
        f"({reduction:.2f}% reduction)"
    )