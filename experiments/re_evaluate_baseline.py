import json
from pathlib import Path

from config import (
    MODEL_NAME,
    DATABASE_ROOT,
    RESULTS_DIR,
)

from src.sql_cleaner import SQLCleaner
from src.sql_executor import SQLExecutor
from src.evaluator import Evaluator
from src.database_manager import DatabaseManager


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = MODEL_NAME

INPUT_FILE = (
    RESULTS_DIR
    / MODEL_NAME.split("/")[-1]
    / "zero_shot_v2.jsonl"
)

OUTPUT_FILE = (
    RESULTS_DIR
    / MODEL_NAME.split("/")[-1]
    / "zero_shot_v2_re_evaluated.jsonl"
)


# ============================================================
# INITIALIZE
# ============================================================

executor = SQLExecutor()
evaluator = Evaluator()
db_manager = DatabaseManager(DATABASE_ROOT)


# ============================================================
# LOAD RESULTS
# ============================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Baseline result file not found:\n{INPUT_FILE}"
    )

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    results = [
        json.loads(line)
        for line in f
        if line.strip()
    ]

print("=" * 60)
print("BASELINE SQL CLEANER RE-EVALUATION")
print("=" * 60)

print("Model:", MODEL_NAME)
print("Original File:")
print(INPUT_FILE)

print("\nOutput File:")
print(OUTPUT_FILE)

print("\nQuestions Loaded:", len(results))


# ============================================================
# RE-EVALUATE
# ============================================================

re_evaluated = []

original_correct = 0
new_correct = 0

changed_questions = []


for result in results:

    question_id = result["question_id"]
    db_id = result["db_id"]

    original_sql = result["generated_sql"]

    # --------------------------------------------------------
    # Clean generated SQL
    # --------------------------------------------------------

    cleaned_sql = SQLCleaner.clean(original_sql)

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    database_path = db_manager.get_database_path(db_id)

    # --------------------------------------------------------
    # Execute generated SQL
    # --------------------------------------------------------

    generated_result = executor.execute(
        database_path,
        cleaned_sql
    )

    # --------------------------------------------------------
    # Gold result
    # --------------------------------------------------------

    gold_result = executor.execute(
        database_path,
        result["gold_sql"]
    )

    # --------------------------------------------------------
    # Recalculate execution accuracy
    # --------------------------------------------------------

    execution_accuracy = evaluator.execution_accuracy(
        gold_result,
        generated_result
    )

    original_accuracy = result["execution_accuracy"]

    if original_accuracy:
        original_correct += 1

    if execution_accuracy:
        new_correct += 1

    # --------------------------------------------------------
    # Track accuracy changes
    # --------------------------------------------------------

    if original_accuracy != execution_accuracy:

        changed_questions.append(
            {
                "question_id": question_id,
                "original_accuracy": original_accuracy,
                "new_accuracy": execution_accuracy,
                "original_sql": original_sql,
                "cleaned_sql": cleaned_sql,
                "error": generated_result.error,
            }
        )

        print("\n" + "-" * 60)
        print("QUESTION", question_id)

        print(
            "Accuracy:",
            original_accuracy,
            "->",
            execution_accuracy
        )

        print("\nORIGINAL SQL:")
        print(original_sql)

        print("\nCLEANED SQL:")
        print(cleaned_sql)

        print("\nERROR:")
        print(generated_result.error)

    # --------------------------------------------------------
    # Store updated result
    # --------------------------------------------------------

    updated_result = result.copy()

    updated_result["generated_sql"] = cleaned_sql

    updated_result["execution_accuracy"] = execution_accuracy

    updated_result["valid_sql"] = generated_result.success

    updated_result["generated_result"] = generated_result.rows

    updated_result["error"] = generated_result.error

    re_evaluated.append(updated_result)


# ============================================================
# SAVE
# ============================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for result in re_evaluated:

        json.dump(
            result,
            f,
            ensure_ascii=False
        )

        f.write("\n")


# ============================================================
# SUMMARY
# ============================================================

total = len(results)

original_accuracy_percent = (
    original_correct / total * 100
    if total > 0
    else 0
)

new_accuracy_percent = (
    new_correct / total * 100
    if total > 0
    else 0
)


print("\n")
print("=" * 60)
print("RE-EVALUATION SUMMARY")
print("=" * 60)

print(f"Total Questions: {total}")

print(
    f"Original Correct: "
    f"{original_correct}/{total}"
)

print(
    f"Original Accuracy: "
    f"{original_accuracy_percent:.2f}%"
)

print(
    f"Re-evaluated Correct: "
    f"{new_correct}/{total}"
)

print(
    f"Re-evaluated Accuracy: "
    f"{new_accuracy_percent:.2f}%"
)

print(
    f"Accuracy Changed: "
    f"{len(changed_questions)}"
)

if changed_questions:

    print("\nQuestion IDs:")

    print(
        [
            item["question_id"]
            for item in changed_questions
        ]
    )

print("\nSaved Re-evaluated Results:")

print(OUTPUT_FILE)

print("=" * 60)