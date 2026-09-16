import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = Path(
    "analysis/final_error_taxonomy/"
    "publication_ready_error_taxonomy_summary.csv"
)

OUTPUT_DIR = Path("analysis/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "semantic_error_distribution.png"


# ============================================================
# Load data
# ============================================================

df = pd.read_csv(INPUT_FILE)

# Remove Total row
df = df[df["Error category"] != "Total"].copy()

# Sort from largest to smallest
df = df.sort_values("Cases", ascending=True)


# ============================================================
# Create figure
# ============================================================

fig, ax = plt.subplots(figsize=(9, 6))

bars = ax.barh(
    df["Error category"],
    df["Cases"]
)


# Add percentage labels
for bar, percentage in zip(bars, df["Percentage"]):
    ax.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{percentage:.2f}%",
        va="center",
        fontsize=10
    )


# ============================================================
# Formatting
# ============================================================

ax.set_xlabel("Number of semantic-error cases")
ax.set_ylabel("Error category")

ax.set_title(
    "Distribution of Semantic Error Categories",
    fontsize=14,
    pad=12
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.3
)

ax.set_axisbelow(True)

plt.tight_layout()


# ============================================================
# Save
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("=" * 70)
print("Semantic error taxonomy figure created")
print("=" * 70)
print(f"Saved to: {OUTPUT_FILE}")