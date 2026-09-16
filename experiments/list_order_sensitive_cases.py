import csv
from pathlib import Path


INPUT_DIR = Path("analysis/result_validation")

OUTPUT_FILE = (
    INPUT_DIR / "all_order_sensitive_cases.csv"
)


rows = []


for file in sorted(INPUT_DIR.glob("*_validated.csv")):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for record in reader:

            if record["classification"] in {
                "same_rows_order_diff",
                "same_rows_order_diff_order_sensitive"
            }:

                record["source_file"] = file.name
                rows.append(record)


# ------------------------------------------------------------
# PRINT
# ------------------------------------------------------------

print("=" * 80)
print("ORDER-SENSITIVE / ORDER-DIFFERENCE CASES")
print("=" * 80)

for row in rows:

    print("=" * 80)

    print(
        f"Experiment     : {row['experiment']}"
    )

    print(
        f"Question ID    : {row['question_id']}"
    )

    print(
        f"Database       : {row['db_id']}"
    )

    print(
        f"Classification  : {row['classification']}"
    )

    print(
        f"Gold ORDER BY   : {row['gold_has_order_by']}"
    )

    print(
        f"Generated ORDER : {row['generated_has_order_by']}"
    )

    print()

    print("QUESTION:")
    print(row["question"])

    print()

    print("GOLD SQL:")
    print(row["gold_sql"])

    print()

    print("GENERATED SQL:")
    print(row["generated_sql"])

    print()


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

fieldnames = [
    "source_file",
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
    writer.writerows(rows)


print()
print("=" * 80)
print(f"Total cases: {len(rows)}")
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 80)