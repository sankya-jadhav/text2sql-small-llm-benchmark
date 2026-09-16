import csv
import sqlite3
from pathlib import Path
from collections import Counter


# ============================================================
# CONFIGURATION
# ============================================================

RESULTS_ROOT = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results"
)

DATABASE_ROOT = Path(
    "/content/drive/MyDrive/spider_data/spider_data/database"
)

INPUT_DIR = Path("analysis/valid_wrong")

OUTPUT_DIR = Path("analysis/result_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


FILES = [
    "Qwen_ZeroShot_valid_wrong.csv",
    "Qwen_Pruning_valid_wrong.csv",
    "Qwen_Hybrid_valid_wrong.csv",
    "DeepSeek_ZeroShot_valid_wrong.csv",
    "DeepSeek_Hybrid_valid_wrong.csv",
    "Llama_ZeroShot_valid_wrong.csv",
    "Llama_Hybrid_valid_wrong.csv",
]


# ============================================================
# HELPERS
# ============================================================

def execute_sql(db_path, sql):

    connection = sqlite3.connect(db_path)

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    finally:
        connection.close()


def has_order_by(sql):

    return "order by" in sql.lower()


def same_unordered_result(gold_rows, generated_rows):

    return Counter(gold_rows) == Counter(generated_rows)


def classify_result(
    gold_rows,
    generated_rows,
    gold_sql,
    generated_sql
):

    # Exact evaluator-style comparison
    if gold_rows == generated_rows:
        return "exact_same_result"

    # Ignore row order
    if same_unordered_result(
        gold_rows,
        generated_rows
    ):

        if (
            has_order_by(gold_sql)
            or has_order_by(generated_sql)
        ):
            return "same_rows_order_diff_order_sensitive"

        return "same_rows_order_diff"

    return "different_results"


# ============================================================
# PROCESS FILES
# ============================================================

summary = []


for filename in FILES:

    input_file = INPUT_DIR / filename

    if not input_file.exists():
        print(f"Skipping missing file: {input_file}")
        continue

    print("=" * 70)
    print(filename)

    rows = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for record in reader:

            db_id = record["db_id"]

            db_path = (
                DATABASE_ROOT
                / db_id
                / f"{db_id}.sqlite"
            )

            try:

                gold_rows = execute_sql(
                    db_path,
                    record["gold_sql"]
                )

                generated_rows = execute_sql(
                    db_path,
                    record["generated_sql"]
                )

                classification = classify_result(
                    gold_rows,
                    generated_rows,
                    record["gold_sql"],
                    record["generated_sql"]
                )

                rows.append({
                    "experiment":
                        record["experiment"],

                    "question_id":
                        record["question_id"],

                    "db_id":
                        db_id,

                    "question":
                        record["question"],

                    "classification":
                        classification,

                    "gold_row_count":
                        len(gold_rows),

                    "generated_row_count":
                        len(generated_rows),

                    "gold_has_order_by":
                        has_order_by(record["gold_sql"]),

                    "generated_has_order_by":
                        has_order_by(
                            record["generated_sql"]
                        ),

                    "gold_sql":
                        record["gold_sql"],

                    "generated_sql":
                        record["generated_sql"],
                })

            except Exception as e:

                rows.append({
                    "experiment":
                        record["experiment"],

                    "question_id":
                        record["question_id"],

                    "db_id":
                        db_id,

                    "question":
                        record["question"],

                    "classification":
                        "execution_error_during_diagnostic",

                    "gold_row_count":
                        None,

                    "generated_row_count":
                        None,

                    "gold_has_order_by":
                        has_order_by(record["gold_sql"]),

                    "generated_has_order_by":
                        has_order_by(
                            record["generated_sql"]
                        ),

                    "gold_sql":
                        record["gold_sql"],

                    "generated_sql":
                        record["generated_sql"],
                })

                print(
                    f"Diagnostic error Q{record['question_id']}: "
                    f"{e}"
                )


    # ========================================================
    # SAVE FILE
    # ========================================================

    output_file = (
        OUTPUT_DIR /
        filename.replace(
            ".csv",
            "_validated.csv"
        )
    )

    fieldnames = [
        "experiment",
        "question_id",
        "db_id",
        "question",
        "classification",
        "gold_row_count",
        "generated_row_count",
        "gold_has_order_by",
        "generated_has_order_by",
        "gold_sql",
        "generated_sql",
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
        writer.writerows(rows)


    # ========================================================
    # SUMMARY
    # ========================================================

    counts = Counter(
        row["classification"]
        for row in rows
    )

    print()

    for category, count in counts.items():

        print(
            f"{category:40s} {count}"
        )

    summary.append({
        "experiment":
            filename.replace(
                "_valid_wrong.csv",
                ""
            ),

        "exact_same_result":
            counts["exact_same_result"],

        "same_rows_order_diff":
            counts["same_rows_order_diff"],

        "same_rows_order_diff_order_sensitive":
            counts[
                "same_rows_order_diff_order_sensitive"
            ],

        "different_results":
            counts["different_results"],

        "diagnostic_errors":
            counts[
                "execution_error_during_diagnostic"
            ],
    })


# ============================================================
# SAVE SUMMARY
# ============================================================

summary_file = (
    OUTPUT_DIR /
    "result_validation_summary.csv"
)

with open(
    summary_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    fieldnames = [
        "experiment",
        "exact_same_result",
        "same_rows_order_diff",
        "same_rows_order_diff_order_sensitive",
        "different_results",
        "diagnostic_errors",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(summary)


print()
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

for item in summary:

    print(
        f"{item['experiment']:25s}"
        f" exact={item['exact_same_result']:3d}"
        f" unordered={item['same_rows_order_diff']:3d}"
        f" order_sensitive={item['same_rows_order_diff_order_sensitive']:3d}"
        f" different={item['different_results']:3d}"
    )