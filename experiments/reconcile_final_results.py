import json
from pathlib import Path
from collections import defaultdict


# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results"
)

OUTPUT_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results/reconciled"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# AUTHORITATIVE RESULT FILES
# ============================================================

EXPERIMENT_FILES = {
    "Qwen_ZeroShot": (
        RESULTS_DIR
        / "Qwen2.5-Coder-7B-Instruct"
        / "zero_shot_v2_re_evaluated.jsonl"
    ),

    "Qwen_Pruning": (
        RESULTS_DIR
        / "Qwen2.5-Coder-7B-Instruct"
        / "zero_shot_v2_pruned_re_evaluated.jsonl"
    ),

    "Qwen_Hybrid": (
        RESULTS_DIR
        / "Qwen2.5-Coder-7B-Instruct"
        / "hybrid_v1.jsonl"
    ),

    "DeepSeek_ZeroShot": (
        RESULTS_DIR
        / "deepseek-coder-6.7b-instruct"
        / "deepseek_zero_shot_v2.jsonl"
    ),

    "DeepSeek_Hybrid": (
        RESULTS_DIR
        / "deepseek-coder-6.7b-instruct"
        / "deepseek_hybrid_v2.jsonl"
    ),

    "Llama_ZeroShot": (
        RESULTS_DIR
        / "Llama-3.1-8B-Instruct"
        / "llama_zero_shot_v2.jsonl"
    ),

    "Llama_Hybrid": (
        RESULTS_DIR
        / "Llama-3.1-8B-Instruct"
        / "llama_hybrid_v1.jsonl"
    ),
}


# ============================================================
# EVALUATION-SENSITIVE ORDER CASES
#
# These are cases where the generated and gold result sets
# contained the same rows but differed only in order, and
# ordering was not semantically required.
#
# IMPORTANT:
# Q580 is intentionally NOT included because those cases
# were confirmed to be genuinely ORDER BY-sensitive.
# ============================================================

ORDER_ONLY_CASES = {
    "DeepSeek_Hybrid": {35, 243, 405, 1022, 1023},
    "DeepSeek_ZeroShot": {405, 1022, 1023},

    "Llama_Hybrid": {35, 405, 918, 1022, 1023},
    "Llama_ZeroShot": {35, 918, 1022, 1023},

    "Qwen_Hybrid": {911, 1022, 1023},
    "Qwen_Pruning": {918, 1022, 1023},
    "Qwen_ZeroShot": {1022, 1023},
}


# ============================================================
# EVALUATOR TYPE ARTIFACTS
#
# Q420 occurred in every one of the seven conditions.
# Gold/generated results differed only because of numeric
# representation/type, e.g. 3 vs 3.0 vs "3".
# ============================================================

TYPE_ARTIFACT_CASES = {
    experiment: {420}
    for experiment in EXPERIMENT_FILES
}


# ============================================================
# HELPERS
# ============================================================

def normalize_value(value):
    """
    Normalize values for evaluator-level comparison.

    Numeric values such as:
        3
        3.0
        "3"

    are treated as equivalent where possible.

    This is used ONLY for identifying evaluator artifacts.
    It does not modify generated SQL.
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        stripped = value.strip()

        try:
            return float(stripped)
        except ValueError:
            return stripped

    return value


def normalize_rows(rows):
    normalized = []

    for row in rows:
        normalized_row = tuple(
            normalize_value(value)
            for value in row
        )
        normalized.append(normalized_row)

    return normalized


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


# ============================================================
# RECONCILIATION
# ============================================================

all_results = {}

for experiment, path in EXPERIMENT_FILES.items():

    print("=" * 80)
    print(f"Loading: {experiment}")
    print(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Result file not found: {path}"
        )

    rows = load_jsonl(path)

    print(f"Rows: {len(rows)}")

    if len(rows) != 180:
        raise ValueError(
            f"{experiment} has {len(rows)} rows, expected 180."
        )

    all_results[experiment] = rows


# ============================================================
# APPLY RECONCILIATION
# ============================================================

summary = []

changed_cases = []

for experiment, rows in all_results.items():

    old_correct = 0
    new_correct = 0

    order_corrected = 0
    type_corrected = 0

    output_rows = []

    for result in rows:

        question_id = result["question_id"]

        old_accuracy = bool(
            result["execution_accuracy"]
        )

        new_accuracy = old_accuracy

        reconciliation_reason = None

        # ----------------------------------------------------
        # 1. Order-only evaluator cases
        # ----------------------------------------------------

        if question_id in ORDER_ONLY_CASES.get(
            experiment, set()
        ):
            new_accuracy = True
            reconciliation_reason = (
                "evaluation_sensitive_order_only"
            )
            order_corrected += 1

        # ----------------------------------------------------
        # 2. Numeric/type evaluator artifacts
        # ----------------------------------------------------

        elif question_id in TYPE_ARTIFACT_CASES.get(
            experiment, set()
        ):

            gold_result = result.get(
                "gold_result", []
            )

            generated_result = result.get(
                "generated_result", []
            )

            normalized_gold = normalize_rows(
                gold_result
            )

            normalized_generated = normalize_rows(
                generated_result
            )

            if normalized_gold == normalized_generated:
                new_accuracy = True
                reconciliation_reason = (
                    "evaluator_type_artifact"
                )
                type_corrected += 1

        # ----------------------------------------------------
        # Preserve everything else
        # ----------------------------------------------------

        if old_accuracy:
            old_correct += 1

        if new_accuracy:
            new_correct += 1

        if old_accuracy != new_accuracy:

            changed_cases.append({
                "experiment": experiment,
                "question_id": question_id,
                "old_execution_accuracy": old_accuracy,
                "new_execution_accuracy": new_accuracy,
                "reason": reconciliation_reason,
            })

        result["original_execution_accuracy"] = (
            old_accuracy
        )

        result["reconciled_execution_accuracy"] = (
            new_accuracy
        )

        result["reconciliation_applied"] = (
            reconciliation_reason is not None
        )

        result["reconciliation_reason"] = (
            reconciliation_reason
        )

        # Keep the original field unchanged for now.
        #
        # This is deliberate: we want the new field to be
        # auditable before replacing the original metric.

        output_rows.append(result)

    # --------------------------------------------------------
    # Save reconciled file
    # --------------------------------------------------------

    output_file = (
        OUTPUT_DIR
        / f"{experiment}_reconciled.jsonl"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        for result in output_rows:
            json.dump(
                result,
                f,
                ensure_ascii=False
            )
            f.write("\n")

    summary.append({
        "experiment": experiment,
        "total": len(rows),
        "old_correct": old_correct,
        "old_accuracy": old_correct / len(rows) * 100,
        "new_correct": new_correct,
        "new_accuracy": new_correct / len(rows) * 100,
        "accuracy_change_pp": (
            (new_correct - old_correct)
            / len(rows)
            * 100
        ),
        "order_cases_reclassified": order_corrected,
        "type_artifacts_reclassified": type_corrected,
        "total_reclassified": (
            order_corrected + type_corrected
        ),
        "output_file": str(output_file),
    })


# ============================================================
# PRINT SUMMARY
# ============================================================

print("\n")
print("=" * 100)
print("FINAL RECONCILIATION SUMMARY")
print("=" * 100)

for item in summary:

    print(
        f"{item['experiment']:<22}"
        f"Old: {item['old_correct']:>3}/180 "
        f"({item['old_accuracy']:>6.2f}%)   "
        f"New: {item['new_correct']:>3}/180 "
        f"({item['new_accuracy']:>6.2f}%)   "
        f"Change: {item['accuracy_change_pp']:>+6.2f} pp   "
        f"Reclassified: {item['total_reclassified']}"
    )


print("\n")
print("=" * 100)
print("CHANGED CASES")
print("=" * 100)

for case in changed_cases:
    print(
        f"{case['experiment']:<22}"
        f"Q{case['question_id']:<5}"
        f"{case['old_execution_accuracy']} -> "
        f"{case['new_execution_accuracy']}   "
        f"{case['reason']}"
    )


print("\n")
print("=" * 100)
print("TOTAL")
print("=" * 100)

old_total_correct = sum(
    item["old_correct"]
    for item in summary
)

new_total_correct = sum(
    item["new_correct"]
    for item in summary
)

total_runs = 7 * 180

print(
    f"Old correct: "
    f"{old_total_correct}/{total_runs} "
    f"({old_total_correct / total_runs * 100:.2f}%)"
)

print(
    f"New correct: "
    f"{new_total_correct}/{total_runs} "
    f"({new_total_correct / total_runs * 100:.2f}%)"
)

print(
    f"Overall change: "
    f"{(new_total_correct - old_total_correct) / total_runs * 100:+.2f} pp"
)

print()
print(
    f"Order-only reclassified: "
    f"{sum(item['order_cases_reclassified'] for item in summary)}"
)

print(
    f"Type artifacts reclassified: "
    f"{sum(item['type_artifacts_reclassified'] for item in summary)}"
)

print(
    f"Total reclassified: "
    f"{sum(item['total_reclassified'] for item in summary)}"
)

print("\n")
print("Reconciled files saved to:")
print(OUTPUT_DIR)
print("=" * 100)