import json
from pathlib import Path
from statistics import mean

from config import RESULTS_DIR


# ==========================================================
# CONFIGURATION
# ==========================================================

EXPERIMENTS = {
    "Qwen Zero-shot": (
        "Qwen2.5-Coder-7B-Instruct",
        "zero_shot_v2.jsonl",
    ),
    "Qwen Pruning": (
        "Qwen2.5-Coder-7B-Instruct",
        "zero_shot_v2_pruned.jsonl",
    ),
    "Qwen Hybrid": (
        "Qwen2.5-Coder-7B-Instruct",
        "hybrid_v1.jsonl",
    ),
    "DeepSeek Zero-shot": (
        "deepseek-coder-6.7b-instruct",
        "deepseek_zero_shot_v2.jsonl",
    ),
    "DeepSeek Hybrid": (
        "deepseek-coder-6.7b-instruct",
        "deepseek_hybrid_v2.jsonl",
    ),
}


# ==========================================================
# LOAD RESULTS
# ==========================================================

def load_results(model_dir, filename):
    path = RESULTS_DIR / model_dir / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Result file not found:\n{path}"
        )

    with open(path, "r", encoding="utf-8") as f:
        rows = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    return rows


# ==========================================================
# BASIC METRICS
# ==========================================================

def percentage(count, total):
    return (
        count / total * 100
        if total
        else 0.0
    )


def calculate_metrics(rows):
    total = len(rows)

    execution_correct = sum(
        bool(r["execution_accuracy"])
        for r in rows
    )

    exact_match = sum(
        bool(r["exact_match"])
        for r in rows
    )

    valid_sql = sum(
        bool(r["valid_sql"])
        for r in rows
    )

    return {
        "n": total,
        "execution_correct": execution_correct,
        "execution_accuracy": percentage(
            execution_correct,
            total
        ),
        "exact_match_count": exact_match,
        "exact_match": percentage(
            exact_match,
            total
        ),
        "valid_sql_count": valid_sql,
        "valid_sql": percentage(
            valid_sql,
            total
        ),
    }


# ==========================================================
# GENERATION / COST METRICS
# ==========================================================

def average(rows, field):
    values = [
        r[field]
        for r in rows
        if r.get(field) is not None
    ]

    return mean(values) if values else 0.0


def calculate_generation_metrics(rows):
    return {
        "latency": average(
            rows,
            "latency"
        ),
        "prompt_tokens": average(
            rows,
            "prompt_tokens"
        ),
        "completion_tokens": average(
            rows,
            "completion_tokens"
        ),
        "total_tokens": average(
            rows,
            "total_tokens"
        ),
    }


# ==========================================================
# SCHEMA METRICS
# ==========================================================

def calculate_schema_metrics(rows):
    reductions = [
        r["schema_reduction_percent"]
        for r in rows
        if r.get("schema_reduction_percent")
        is not None
    ]

    full_columns = [
        r["full_schema_columns"]
        for r in rows
        if r.get("full_schema_columns")
        is not None
    ]

    pruned_columns = [
        r["pruned_schema_columns"]
        for r in rows
        if r.get("pruned_schema_columns")
        is not None
    ]

    if not reductions:
        return None

    return {
        "schema_reduction": mean(
            reductions
        ),
        "full_columns": mean(
            full_columns
        ),
        "pruned_columns": mean(
            pruned_columns
        ),
    }


# ==========================================================
# FEEDBACK METRICS
# ==========================================================

def calculate_feedback_metrics(rows):
    if not any(
        "was_corrected" in r
        for r in rows
    ):
        return None

    initial_failures = sum(
        r.get("initial_execution_success")
        is False
        for r in rows
    )

    feedback_attempts = sum(
        bool(r.get("was_corrected"))
        for r in rows
    )

    feedback_valid = sum(
        bool(r.get("was_corrected"))
        and bool(r["valid_sql"])
        for r in rows
    )

    feedback_correct = sum(
        bool(r.get("was_corrected"))
        and bool(r["execution_accuracy"])
        for r in rows
    )

    return {
        "initial_failures": initial_failures,
        "feedback_attempts": feedback_attempts,
        "feedback_valid": feedback_valid,
        "feedback_correct": feedback_correct,
    }


# ==========================================================
# PAIRWISE COMPARISON
# ==========================================================

def compare_experiments(
    name_a,
    rows_a,
    name_b,
    rows_b
):
    a = {
        r["question_id"]: r
        for r in rows_a
    }

    b = {
        r["question_id"]: r
        for r in rows_b
    }

    common_ids = sorted(
        set(a) & set(b)
    )

    both_correct = []
    a_correct_b_wrong = []
    a_wrong_b_correct = []
    both_wrong = []

    for qid in common_ids:

        a_correct = bool(
            a[qid]["execution_accuracy"]
        )

        b_correct = bool(
            b[qid]["execution_accuracy"]
        )

        if a_correct and b_correct:
            both_correct.append(qid)

        elif a_correct and not b_correct:
            a_correct_b_wrong.append(qid)

        elif not a_correct and b_correct:
            a_wrong_b_correct.append(qid)

        else:
            both_wrong.append(qid)

    print()
    print("=" * 70)
    print(
        f"{name_a}  VS  {name_b}"
    )
    print("=" * 70)

    print(
        f"Common questions: "
        f"{len(common_ids)}"
    )

    print(
        f"Both correct       : "
        f"{len(both_correct)}"
    )

    print(
        f"{name_a} correct / "
        f"{name_b} wrong: "
        f"{len(a_correct_b_wrong)}"
    )

    print(
        f"{name_a} wrong / "
        f"{name_b} correct: "
        f"{len(a_wrong_b_correct)}"
    )

    print(
        f"Both wrong         : "
        f"{len(both_wrong)}"
    )

    print()
    print(
        "A → B net change: "
        f"{len(a_wrong_b_correct) - len(a_correct_b_wrong):+d}"
    )


# ==========================================================
# MAIN REPORT
# ==========================================================

def main():

    loaded = {}

    for name, (
        model_dir,
        filename
    ) in EXPERIMENTS.items():

        rows = load_results(
            model_dir,
            filename
        )

        loaded[name] = rows

    print()
    print("#" * 70)
    print("TEXT-TO-SQL BENCHMARK ANALYSIS")
    print("#" * 70)

    # ------------------------------------------------------
    # MAIN METRICS
    # ------------------------------------------------------

    print()
    print("=" * 70)
    print("MAIN METRICS")
    print("=" * 70)

    for name, rows in loaded.items():

        metrics = calculate_metrics(
            rows
        )

        print()
        print(name)

        print(
            f"  N                  : "
            f"{metrics['n']}"
        )

        print(
            f"  Execution Accuracy : "
            f"{metrics['execution_correct']}/"
            f"{metrics['n']} "
            f"({metrics['execution_accuracy']:.2f}%)"
        )

        print(
            f"  Exact Match        : "
            f"{metrics['exact_match_count']}/"
            f"{metrics['n']} "
            f"({metrics['exact_match']:.2f}%)"
        )

        print(
            f"  Valid SQL          : "
            f"{metrics['valid_sql_count']}/"
            f"{metrics['n']} "
            f"({metrics['valid_sql']:.2f}%)"
        )

    # ------------------------------------------------------
    # GENERATION METRICS
    # ------------------------------------------------------

    print()
    print("=" * 70)
    print("GENERATION / COST METRICS")
    print("=" * 70)

    for name, rows in loaded.items():

        metrics = calculate_generation_metrics(
            rows
        )

        print()
        print(name)

        print(
            f"  Avg latency       : "
            f"{metrics['latency']:.4f}s"
        )

        print(
            f"  Avg prompt tokens : "
            f"{metrics['prompt_tokens']:.2f}"
        )

        print(
            f"  Avg completion    : "
            f"{metrics['completion_tokens']:.2f}"
        )

        print(
            f"  Avg total tokens  : "
            f"{metrics['total_tokens']:.2f}"
        )

    # ------------------------------------------------------
    # SCHEMA METRICS
    # ------------------------------------------------------

    print()
    print("=" * 70)
    print("SCHEMA PRUNING")
    print("=" * 70)

    for name, rows in loaded.items():

        metrics = calculate_schema_metrics(
            rows
        )

        if metrics is None:
            continue

        print()
        print(name)

        print(
            f"  Avg full columns   : "
            f"{metrics['full_columns']:.2f}"
        )

        print(
            f"  Avg pruned columns : "
            f"{metrics['pruned_columns']:.2f}"
        )

        print(
            f"  Avg reduction      : "
            f"{metrics['schema_reduction']:.2f}%"
        )

    # ------------------------------------------------------
    # FEEDBACK METRICS
    # ------------------------------------------------------

    print()
    print("=" * 70)
    print("EXECUTION FEEDBACK")
    print("=" * 70)

    for name, rows in loaded.items():

        metrics = calculate_feedback_metrics(
            rows
        )

        if metrics is None:
            continue

        print()
        print(name)

        print(
            f"  Initial failures : "
            f"{metrics['initial_failures']}"
        )

        print(
            f"  Feedback attempts: "
            f"{metrics['feedback_attempts']}"
        )

        print(
            f"  Became valid     : "
            f"{metrics['feedback_valid']}"
        )

        print(
            f"  Became correct   : "
            f"{metrics['feedback_correct']}"
        )

    # ------------------------------------------------------
    # QWEN COMPARISONS
    # ------------------------------------------------------

    compare_experiments(
        "Qwen Zero-shot",
        loaded["Qwen Zero-shot"],
        "Qwen Pruning",
        loaded["Qwen Pruning"]
    )

    compare_experiments(
        "Qwen Zero-shot",
        loaded["Qwen Zero-shot"],
        "Qwen Hybrid",
        loaded["Qwen Hybrid"]
    )

    compare_experiments(
        "Qwen Pruning",
        loaded["Qwen Pruning"],
        "Qwen Hybrid",
        loaded["Qwen Hybrid"]
    )

    # ------------------------------------------------------
    # DEEPSEEK COMPARISON
    # ------------------------------------------------------

    compare_experiments(
        "DeepSeek Zero-shot",
        loaded["DeepSeek Zero-shot"],
        "DeepSeek Hybrid",
        loaded["DeepSeek Hybrid"]
    )


if __name__ == "__main__":
    main()