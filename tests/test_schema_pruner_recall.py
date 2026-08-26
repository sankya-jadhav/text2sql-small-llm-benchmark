import json
import re

from config import TABLES_JSON
from src.dataset_loader import DatasetLoader
from src.schema_extractor import SchemaExtractor
from src.schema_pruner import SchemaPruner


# ==========================================================
# GOLD TABLE EXTRACTION
# ==========================================================

def extract_gold_tables(sql):
    """
    Extract table names referenced after FROM or JOIN.

    This is a lightweight validation helper for checking whether
    the schema pruner retained tables required by the gold SQL.
    """

    sql = sql.lower()

    pattern = r"\b(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)"

    tables = re.findall(
        pattern,
        sql
    )

    return set(tables)


# ==========================================================
# MAIN VALIDATION
# ==========================================================

def test_schema_pruner_recall():

    # ------------------------------------------------------
    # Load dataset metadata
    # ------------------------------------------------------

    loader = DatasetLoader(
        "data/dev.json",
        TABLES_JSON
    )

    extractor = SchemaExtractor(
        loader.tables_data
    )

    pruner = SchemaPruner()

    # ------------------------------------------------------
    # Load 180-question benchmark
    # ------------------------------------------------------

    with open(
        "data/benchmark_sample_180.json",
        "r",
        encoding="utf-8"
    ) as f:

        benchmark = json.load(f)

    total_questions = 0

    questions_with_all_gold_tables = 0

    failures = []

    # ------------------------------------------------------
    # Evaluate every question
    # ------------------------------------------------------

    for question_index, sample in enumerate(benchmark):

        total_questions += 1

        db_id = sample["db_id"]

        question = sample["question"]

        gold_sql = sample["query"]

        # --------------------------------------------------
        # Get original schema
        # --------------------------------------------------

        schema = extractor.get_schema(
            db_id
        )

        # --------------------------------------------------
        # Run pruner
        # --------------------------------------------------

        pruned_schema = pruner.prune(
            schema,
            question
        )

        pruned_tables = set(
            table.lower()
            for table in pruned_schema["tables"]
        )

        # --------------------------------------------------
        # Extract tables required by gold SQL
        # --------------------------------------------------

        gold_tables = extract_gold_tables(
            gold_sql
        )

        # --------------------------------------------------
        # Find missing tables
        # --------------------------------------------------

        missing_tables = (
            gold_tables - pruned_tables
        )

        # --------------------------------------------------
        # Record result
        # --------------------------------------------------

        if not missing_tables:

            questions_with_all_gold_tables  += 1

        else:

            failures.append({

                "question_index": question_index,

                "db_id": db_id,

                "question": question,

                "gold_sql": gold_sql,

                "gold_tables": sorted(
                    gold_tables
                ),

                "pruned_tables": sorted(
                    pruned_tables
                ),

                "missing_tables": sorted(
                    missing_tables
                )

            })

    # ======================================================
    # RESULTS
    # ======================================================

    recall = (
        questions_with_all_gold_tables 
        / total_questions
        * 100
    )

    print()

    print("=" * 60)

    print("SCHEMA PRUNER GOLD TABLE RECALL")

    print("=" * 60)

    print(
        f"Total Questions      : {total_questions}"
    )

    print(
        f"Questions With All Gold Tables : "
        f"{questions_with_all_gold_tables }"
    )

    print(
        f"Failures             : "
        f"{len(failures)}"
    )

    print(
        f"Gold Table Recall    : "
        f"{recall:.2f}%"
    )

    print("=" * 60)

    # ======================================================
    # FAILURE DETAILS
    # ======================================================

    if failures:

        print()

        print("FAILURE DETAILS")

        print("=" * 60)

        for failure in failures:

            print()

            print(
                f"Question Index : "
                f"{failure['question_index']}"
            )

            print(
                f"Database       : "
                f"{failure['db_id']}"
            )

            print(
                f"Question       : "
                f"{failure['question']}"
            )

            print()

            print(
                "Gold Tables    :",
                failure["gold_tables"]
            )

            print(
                "Pruned Tables  :",
                failure["pruned_tables"]
            )

            print(
                "Missing Tables :",
                failure["missing_tables"]
            )

            print()

            print(
                "Gold SQL:"
            )

            print(
                failure["gold_sql"]
            )

            print("-" * 60)

    # ======================================================
    # ASSERTION
    # ======================================================

    assert total_questions == 180


if __name__ == "__main__":

    test_schema_pruner_recall()
