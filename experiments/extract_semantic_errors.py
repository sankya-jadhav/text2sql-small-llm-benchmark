import pandas as pd
from pathlib import Path


VALID_WRONG_DIR = Path("analysis/valid_wrong")
ORDER_FILE = Path(
    "analysis/result_validation/all_order_sensitive_cases.csv"
)

OUTPUT_DIR = Path("analysis/final_error_taxonomy")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 1. Load the 29 order-difference cases
# ---------------------------------------------------------

order_df = pd.read_csv(ORDER_FILE)


# ---------------------------------------------------------
# 2. Keep ONLY the 25 evaluation-sensitive cases
#
# These are:
# same_rows_order_diff
#
# We deliberately keep:
# same_rows_order_diff_order_sensitive
# because those contain explicit ORDER BY differences.
# ---------------------------------------------------------

evaluation_sensitive_df = order_df[
    order_df["classification"] == "same_rows_order_diff"
].copy()


evaluation_sensitive = set(
    zip(
        evaluation_sensitive_df["experiment"],
        evaluation_sensitive_df["question_id"]
    )
)


print("=" * 80)
print("EVALUATION-SENSITIVE CASES")
print("=" * 80)

print(
    f"Found {len(evaluation_sensitive)} "
    "evaluation-sensitive cases"
)


# ---------------------------------------------------------
# 3. Load all 7 valid-but-wrong files
# ---------------------------------------------------------

all_rows = []

csv_files = sorted(
    VALID_WRONG_DIR.glob("*_valid_wrong.csv")
)

print("\nFiles:")

for file in csv_files:

    df = pd.read_csv(file)

    print(
        f"  {file.name:<45}"
        f"{len(df):>4}"
    )

    all_rows.append(df)


all_df = pd.concat(
    all_rows,
    ignore_index=True
)


print(
    f"\nTotal valid-but-wrong cases: "
    f"{len(all_df)}"
)


# ---------------------------------------------------------
# 4. Mark evaluation-sensitive cases
# ---------------------------------------------------------

def is_evaluation_sensitive(row):

    key = (
        row["experiment"],
        int(row["question_id"])
    )

    return key in evaluation_sensitive


all_df["is_evaluation_sensitive"] = (
    all_df.apply(
        is_evaluation_sensitive,
        axis=1
    )
)


# ---------------------------------------------------------
# 5. Separate the two groups
# ---------------------------------------------------------

evaluation_df = all_df[
    all_df["is_evaluation_sensitive"]
].copy()


semantic_df = all_df[
    ~all_df["is_evaluation_sensitive"]
].copy()


# ---------------------------------------------------------
# 6. Save both datasets
# ---------------------------------------------------------

evaluation_output = (
    OUTPUT_DIR /
    "evaluation_sensitive_cases.csv"
)

semantic_output = (
    OUTPUT_DIR /
    "semantic_error_cases.csv"
)


evaluation_df.to_csv(
    evaluation_output,
    index=False
)

semantic_df.to_csv(
    semantic_output,
    index=False
)


# ---------------------------------------------------------
# 7. Print final accounting
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("FINAL ACCOUNTING")
print("=" * 80)

print(
    f"Total valid-but-wrong : {len(all_df)}"
)

print(
    f"Evaluation-sensitive  : {len(evaluation_df)}"
)

print(
    f"Semantic-error cases  : {len(semantic_df)}"
)

print(
    f"Check                 : "
    f"{len(evaluation_df)} + {len(semantic_df)} "
    f"= {len(evaluation_df) + len(semantic_df)}"
)

print("=" * 80)


# ---------------------------------------------------------
# 8. Per-experiment counts
# ---------------------------------------------------------

print("\nPER-EXPERIMENT ACCOUNTING")
print("-" * 80)

for experiment in sorted(
    all_df["experiment"].unique()
):

    total = len(
        all_df[
            all_df["experiment"] == experiment
        ]
    )

    evaluation = len(
        evaluation_df[
            evaluation_df["experiment"] == experiment
        ]
    )

    semantic = len(
        semantic_df[
            semantic_df["experiment"] == experiment
        ]
    )

    print(
        f"{experiment:<20}"
        f"Total={total:>3}   "
        f"Evaluation-sensitive={evaluation:>2}   "
        f"Semantic={semantic:>3}"
    )


print("\nSaved files:")
print(evaluation_output)
print(semantic_output)