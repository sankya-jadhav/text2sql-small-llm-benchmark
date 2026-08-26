import json
from pathlib import Path

from config import (
    MODEL_NAME,
    DATABASE_ROOT,
    RESULTS_DIR
)

from src.database_manager import DatabaseManager
from src.sql_executor import SQLExecutor
from src.evaluator import Evaluator
from src.sql_cleaner import SQLCleaner


# ==========================================================
# EXPERIMENT CONFIGURATION
# ==========================================================

STRATEGY = "zero_shot"

# Original experiment
ORIGINAL_PROMPT_VERSION = "v2_pruned"

# New result file
RE_EVALUATED_PROMPT_VERSION = (
    "v2_pruned_re_evaluated"
)


# ==========================================================
# RESULT FILE PATHS
# ==========================================================

safe_model = MODEL_NAME.split("/")[-1]

model_dir = Path(
    RESULTS_DIR
) / safe_model

INPUT_FILE = model_dir / (
    f"{STRATEGY}_"
    f"{ORIGINAL_PROMPT_VERSION}.jsonl"
)

OUTPUT_FILE = model_dir / (
    f"{STRATEGY}_"
    f"{RE_EVALUATED_PROMPT_VERSION}.jsonl"
)


# ==========================================================
# INITIALIZE
# ==========================================================

database_manager = DatabaseManager(
    DATABASE_ROOT
)

sql_executor = SQLExecutor()

evaluator = Evaluator()


# ==========================================================
# CHECK INPUT FILE
# ==========================================================

if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"Original result file not found:\n"
        f"{INPUT_FILE}"
    )


# ==========================================================
# LOAD ORIGINAL RESULTS
# ==========================================================

results = []

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        line = line.strip()

        if line:

            results.append(
                json.loads(line)
            )


print("=" * 60)
print("SQL CLEANER RE-EVALUATION")
print("=" * 60)

print("Model:", MODEL_NAME)

print("Original File:")
print(INPUT_FILE)

print()

print("Output File:")
print(OUTPUT_FILE)

print()

print(
    f"Questions Loaded: "
    f"{len(results)}"
)

print()


# ==========================================================
# RE-EVALUATE
# ==========================================================

updated_results = []

old_correct = 0
new_correct = 0

changed_questions = []

sql_changed_questions = []


for i, result in enumerate(results):

    question_id = result["question_id"]

    db_id = result["db_id"]

    original_sql = result["generated_sql"]

    gold_sql = result["gold_sql"]

    old_accuracy = result[
        "execution_accuracy"
    ]


    # ------------------------------------------------------
    # CLEAN GENERATED SQL
    # ------------------------------------------------------

    cleaned_sql = SQLCleaner.clean(
        original_sql
    )


    # Track whether SQL changed

    if original_sql != cleaned_sql:

        sql_changed_questions.append(
            question_id
        )


    # ------------------------------------------------------
    # GET DATABASE
    # ------------------------------------------------------

    database_path = (
        database_manager.get_database_path(
            db_id
        )
    )


    # ------------------------------------------------------
    # EXECUTE GOLD SQL
    # ------------------------------------------------------

    gold_result = sql_executor.execute(
        database_path,
        gold_sql
    )


    # ------------------------------------------------------
    # EXECUTE CLEANED GENERATED SQL
    # ------------------------------------------------------

    generated_result = sql_executor.execute(
        database_path,
        cleaned_sql
    )


    # ------------------------------------------------------
    # EVALUATE
    # ------------------------------------------------------

    execution_accuracy = (
        evaluator.execution_accuracy(
            gold_result,
            generated_result
        )
    )

    valid_sql = evaluator.valid_sql(
        generated_result
    )

    exact_match = evaluator.exact_match(
        gold_sql,
        cleaned_sql
    )


    # ------------------------------------------------------
    # STATISTICS
    # ------------------------------------------------------

    old_correct += int(
        old_accuracy
    )

    new_correct += int(
        execution_accuracy
    )


    if old_accuracy != execution_accuracy:

        changed_questions.append(
            question_id
        )

        print("-" * 60)

        print(
            f"QUESTION {question_id}"
        )

        print(
            f"Accuracy: "
            f"{old_accuracy} -> "
            f"{execution_accuracy}"
        )

        print()

        print("ORIGINAL SQL:")

        print(original_sql)

        print()

        print("CLEANED SQL:")

        print(cleaned_sql)

        print()

        print("ERROR:")

        print(
            generated_result.error
        )

        print()


    # ------------------------------------------------------
    # UPDATE RESULT
    # ------------------------------------------------------

    result["generated_sql"] = (
        cleaned_sql
    )

    result["execution_accuracy"] = (
        execution_accuracy
    )

    result["exact_match"] = (
        exact_match
    )

    result["valid_sql"] = (
        valid_sql
    )

    result["gold_result"] = (
        gold_result.rows
    )

    result["generated_result"] = (
        generated_result.rows
    )

    result["error"] = (
        generated_result.error
    )


    # Mark this result as re-evaluated

    result["re_evaluated"] = True

    result[
        "original_generated_sql"
    ] = original_sql


    updated_results.append(
        result
    )


# ==========================================================
# SAVE NEW RESULTS
# ==========================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for result in updated_results:

        json.dump(
            result,
            f,
            ensure_ascii=False
        )

        f.write("\n")


# ==========================================================
# SUMMARY
# ==========================================================

total = len(results)

old_accuracy_percent = (
    old_correct / total * 100
    if total > 0
    else 0
)

new_accuracy_percent = (
    new_correct / total * 100
    if total > 0
    else 0
)


print()
print("=" * 60)
print("RE-EVALUATION SUMMARY")
print("=" * 60)

print(
    f"Total Questions: "
    f"{total}"
)

print()

print(
    f"Original Correct: "
    f"{old_correct}/{total}"
)

print(
    f"Original Accuracy: "
    f"{old_accuracy_percent:.2f}%"
)

print()

print(
    f"Re-evaluated Correct: "
    f"{new_correct}/{total}"
)

print(
    f"Re-evaluated Accuracy: "
    f"{new_accuracy_percent:.2f}%"
)

print()

print(
    f"SQL Changed by Cleaner: "
    f"{len(sql_changed_questions)}"
)

print(
    "Question IDs:"
)

print(
    sql_changed_questions
)

print()

print(
    f"Accuracy Changed: "
    f"{len(changed_questions)}"
)

print(
    "Question IDs:"
)

print(
    changed_questions
)

print()

print(
    "Saved Re-evaluated Results:"
)

print(
    OUTPUT_FILE
)