import json
import csv
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results"
)

OUTPUT_DIR = Path("analysis/valid_wrong")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


EXPERIMENTS = {
    "Qwen_ZeroShot": (
        "Qwen2.5-Coder-7B-Instruct",
        "zero_shot_v2_re_evaluated.jsonl"
    ),

    "Qwen_Pruning": (
        "Qwen2.5-Coder-7B-Instruct",
        "zero_shot_v2_pruned_re_evaluated.jsonl"
    ),

    "Qwen_Hybrid": (
        "Qwen2.5-Coder-7B-Instruct",
        "hybrid_v1.jsonl"
    ),

    "DeepSeek_ZeroShot": (
        "deepseek-coder-6.7b-instruct",
        "deepseek_zero_shot_v2.jsonl"
    ),

    "DeepSeek_Hybrid": (
        "deepseek-coder-6.7b-instruct",
        "deepseek_hybrid_v2.jsonl"
    ),

    "Llama_ZeroShot": (
        "Llama-3.1-8B-Instruct",
        "llama_zero_shot_v2.jsonl"
    ),

    "Llama_Hybrid": (
        "Llama-3.1-8B-Instruct",
        "llama_hybrid_v1.jsonl"
    ),
}


# ============================================================
# EXTRACTION
# ============================================================

all_summary = []


for experiment_name, (model_dir, filename) in EXPERIMENTS.items():

    input_file = RESULTS_ROOT / model_dir / filename

    print("=" * 70)
    print(f"Experiment: {experiment_name}")
    print(f"File: {input_file}")

    if not input_file.exists():
        print("WARNING: File not found")
        print()
        continue

    valid_wrong = []

    with open(input_file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            result = json.loads(line)

            # ------------------------------------------------
            # Determine whether SQL was valid/executable
            # ------------------------------------------------

            initial_execution_success = result.get(
                "initial_execution_success"
            )

            if initial_execution_success is None:
                initial_execution_success = result.get(
                    "valid_sql",
                    False
                )

            execution_accuracy = result.get(
                "execution_accuracy",
                False
            )

            # ------------------------------------------------
            # Valid-but-wrong condition
            # ------------------------------------------------

            if (
                initial_execution_success is True
                and execution_accuracy is False
            ):

                valid_wrong.append({
                    "experiment": experiment_name,
                    "question_id": result.get("question_id"),
                    "db_id": result.get("db_id"),
                    "question": result.get("question"),

                    "initial_sql": result.get(
                        "initial_sql",
                        result.get("generated_sql")
                    ),

                    "generated_sql": result.get(
                        "generated_sql"
                    ),

                    "gold_sql": result.get(
                        "gold_sql"
                    ),

                    "initial_execution_success":
                        initial_execution_success,

                    "execution_accuracy":
                        execution_accuracy,

                    "valid_sql":
                        result.get("valid_sql"),

                    "was_corrected":
                        result.get("was_corrected", False),

                    "initial_error":
                        result.get("initial_error"),
                })


    # --------------------------------------------------------
    # Save experiment-specific CSV
    # --------------------------------------------------------

    output_file = (
        OUTPUT_DIR /
        f"{experiment_name}_valid_wrong.csv"
    )

    fieldnames = [
        "experiment",
        "question_id",
        "db_id",
        "question",
        "initial_sql",
        "generated_sql",
        "gold_sql",
        "initial_execution_success",
        "execution_accuracy",
        "valid_sql",
        "was_corrected",
        "initial_error",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(valid_wrong)


    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        f"Valid-but-wrong cases: {len(valid_wrong)}"
    )

    all_summary.append({
        "experiment": experiment_name,
        "valid_wrong_count": len(valid_wrong)
    })


# ============================================================
# SAVE SUMMARY
# ============================================================

summary_file = OUTPUT_DIR / "summary.csv"

with open(
    summary_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "experiment",
            "valid_wrong_count"
        ]
    )

    writer.writeheader()
    writer.writerows(all_summary)


print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

for row in all_summary:
    print(
        f"{row['experiment']:25s} "
        f"{row['valid_wrong_count']}"
    )

print()
print(f"Output directory: {OUTPUT_DIR}")