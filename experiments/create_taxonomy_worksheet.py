import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "analysis/final_error_taxonomy/semantic_error_cases.csv"
)

OUTPUT_FILE = Path(
    "analysis/final_error_taxonomy/"
    "semantic_error_classification_worksheet.csv"
)


df = pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Add empty classification columns
# ---------------------------------------------------------

df["category"] = ""
df["reason"] = ""


# ---------------------------------------------------------
# Keep only the columns needed for manual analysis
# ---------------------------------------------------------

columns = [
    "experiment",
    "question_id",
    "db_id",
    "question",
    "gold_sql",
    "generated_sql",
    "category",
    "reason",
]


worksheet = df[columns].copy()


worksheet.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("=" * 80)
print("5B TAXONOMY WORKSHEET")
print("=" * 80)

print(
    f"Cases: {len(worksheet)}"
)

print(
    f"Experiments: "
    f"{worksheet['experiment'].nunique()}"
)

print()

for experiment, group in worksheet.groupby("experiment"):

    print(
        f"{experiment:<20}"
        f"{len(group):>4} cases"
    )

print()
print("Saved:")
print(OUTPUT_FILE)

print("=" * 80)