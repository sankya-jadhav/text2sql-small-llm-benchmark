import json
from pathlib import Path

from config import RESULTS_DIR, MODEL_NAME


MODEL_DIR = RESULTS_DIR / MODEL_NAME.split("/")[-1]

BASELINE_FILE = MODEL_DIR / "zero_shot_v2_re_evaluated.jsonl"
PRUNED_FILE = MODEL_DIR / "zero_shot_v2_pruned_re_evaluated.jsonl"


def load_results(path):
    with open(path, "r", encoding="utf-8") as f:
        return {
            row["question_id"]: row
            for row in map(json.loads, f)
            if row.strip()
        }


baseline = load_results(BASELINE_FILE)
pruned = load_results(PRUNED_FILE)


assert set(baseline) == set(pruned), (
    "Question IDs do not match between baseline and pruning results."
)


both_correct = []
baseline_correct_pruned_wrong = []
baseline_wrong_pruned_correct = []
both_wrong = []


for question_id in sorted(baseline):

    b = baseline[question_id]["execution_accuracy"]
    p = pruned[question_id]["execution_accuracy"]

    if b and p:
        both_correct.append(question_id)

    elif b and not p:
        baseline_correct_pruned_wrong.append(question_id)

    elif not b and p:
        baseline_wrong_pruned_correct.append(question_id)

    else:
        both_wrong.append(question_id)


print("=" * 60)
print("BASELINE vs PRUNED COMPARISON")
print("=" * 60)

print(f"Total Questions: {len(baseline)}")
print()

print(
    f"Both Correct: "
    f"{len(both_correct)}"
)

print(
    f"Baseline Correct / Pruned Wrong: "
    f"{len(baseline_correct_pruned_wrong)}"
)

print(
    f"Baseline Wrong / Pruned Correct: "
    f"{len(baseline_wrong_pruned_correct)}"
)

print(
    f"Both Wrong: "
    f"{len(both_wrong)}"
)

print()
print("=" * 60)

print("\nBaseline Correct:", sum(
    baseline[q]["execution_accuracy"]
    for q in baseline
))

print("Pruned Correct:", sum(
    pruned[q]["execution_accuracy"]
    for q in pruned
))


print("\n--- HURT CASES ---")
print(baseline_correct_pruned_wrong)


print("\n--- HELPED CASES ---")
print(baseline_wrong_pruned_correct)


print("\n--- BOTH CORRECT ---")
print(both_correct)


print("\n--- BOTH WRONG ---")
print(both_wrong)

print("=" * 60)