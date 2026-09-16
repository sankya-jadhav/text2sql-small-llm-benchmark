import pandas as pd
from pathlib import Path


VALID_WRONG_DIR = Path("analysis/valid_wrong")

csv_files = sorted(
    VALID_WRONG_DIR.glob("*_valid_wrong.csv")
)

print("=" * 80)
print("VALID-BUT-WRONG FILE COVERAGE")
print("=" * 80)

total = 0

for file in csv_files:

    df = pd.read_csv(file)

    print(
        f"{file.name:<45}"
        f"{len(df):>5} cases"
    )

    total += len(df)

print("-" * 80)
print(
    f"{'TOTAL':<45}"
    f"{total:>5} cases"
)

print("=" * 80)