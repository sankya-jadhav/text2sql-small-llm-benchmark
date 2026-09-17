import json
from pathlib import Path
import csv


RESULTS_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results/reconciled"
)

OUTPUT_FILE = Path(
    "analysis/final_results_table.csv"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
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


DISPLAY = {
    "Qwen_ZeroShot": ("Qwen", "Zero-shot"),
    "Qwen_Pruning": ("Qwen", "Pruning"),
    "Qwen_Hybrid": ("Qwen", "Hybrid"),

    "DeepSeek_ZeroShot": ("DeepSeek", "Zero-shot"),
    "DeepSeek_Hybrid": ("DeepSeek", "Hybrid"),

    "Llama_ZeroShot": ("Llama", "Zero-shot"),
    "Llama_Hybrid": ("Llama", "Hybrid"),
}


rows_out = []


for experiment, filename in FILES.items():

    path = RESULTS_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        rows = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    if len(rows) != 180:
        raise ValueError(
            f"{experiment}: expected 180 rows, "
            f"found {len(rows)}"
        )

    model, method = DISPLAY[experiment]

    execution_correct = sum(
        bool(r["reconciled_execution_accuracy"])
        for r in rows
    )

    valid_sql = sum(
        bool(r["valid_sql"])
        for r in rows
    )

    exact_match = sum(
        bool(r["exact_match"])
        for r in rows
    )

    avg_prompt_tokens = sum(
        r.get("prompt_tokens", 0) or 0
        for r in rows
    ) / 180

    avg_completion_tokens = sum(
        r.get("completion_tokens", 0) or 0
        for r in rows
    ) / 180

    avg_total_tokens = sum(
        r.get("total_tokens", 0) or 0
        for r in rows
    ) / 180

    avg_latency = sum(
        r.get("latency", 0) or 0
        for r in rows
    ) / 180

    feedback_triggered = sum(
        r.get("was_corrected") is True
        for r in rows
    )

    feedback_tokens = sum(
        r.get("feedback_total_tokens", 0) or 0
        for r in rows
    )

    feedback_latency = sum(
        r.get("feedback_latency", 0) or 0
        for r in rows
    )

    combined_tokens = (
        sum(
            (r.get("total_tokens", 0) or 0)
            + (r.get("feedback_total_tokens", 0) or 0)
            for r in rows
        )
        / 180
    )

    combined_latency = (
        sum(
            (r.get("latency", 0) or 0)
            + (r.get("feedback_latency", 0) or 0)
            for r in rows
        )
        / 180
    )

    recovered = sum(
        (
            r.get("was_corrected") is True
            and r.get("reconciled_execution_accuracy") is True
            and r.get("initial_execution_success") is False
        )
        for r in rows
    )

    rows_out.append({
        "model": model,
        "method": method,
        "experiment": experiment,
        "n": 180,

        "execution_correct": execution_correct,
        "execution_accuracy_percent":
            execution_correct / 180 * 100,

        "valid_sql_count": valid_sql,
        "valid_sql_percent":
            valid_sql / 180 * 100,

        "exact_match_count": exact_match,
        "exact_match_percent":
            exact_match / 180 * 100,

        "avg_prompt_tokens":
            avg_prompt_tokens,

        "avg_completion_tokens":
            avg_completion_tokens,

        "avg_total_tokens":
            avg_total_tokens,

        "avg_initial_latency_sec":
            avg_latency,

        "feedback_triggered":
            feedback_triggered,

        "feedback_trigger_rate_percent":
            feedback_triggered / 180 * 100,

        "feedback_recovered":
            recovered,

        "feedback_recovery_rate_percent":
            (
                recovered / feedback_triggered * 100
                if feedback_triggered > 0
                else 0
            ),

        "avg_combined_tokens":
            combined_tokens,

        "avg_combined_latency_sec":
            combined_latency,

        "total_feedback_tokens":
            feedback_tokens,

        "total_feedback_latency_sec":
            feedback_latency,
    })


# ------------------------------------------------------------
# Save CSV
# ------------------------------------------------------------

fieldnames = list(rows_out[0].keys())

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows_out)


# ------------------------------------------------------------
# Print
# ------------------------------------------------------------

print("=" * 120)
print("FINAL RESULTS TABLE")
print("=" * 120)

for row in rows_out:

    print(
        f"{row['model']:<12}"
        f"{row['method']:<12}"
        f"Exec: {row['execution_accuracy_percent']:>6.2f}%   "
        f"Valid: {row['valid_sql_percent']:>6.2f}%   "
        f"EM: {row['exact_match_percent']:>6.2f}%   "
        f"Prompt: {row['avg_prompt_tokens']:>7.2f}   "
        f"Total: {row['avg_total_tokens']:>7.2f}"
    )


print()
print("Saved:")
print(OUTPUT_FILE)
print("=" * 120)