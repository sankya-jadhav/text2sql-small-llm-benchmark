import json
from pathlib import Path


RESULTS_DIR = Path(
    "/content/drive/MyDrive/spider_data/spider_data/results/reconciled"
)


HYBRID_FILES = {
    "Qwen": RESULTS_DIR / "Qwen_Hybrid_reconciled.jsonl",
    "DeepSeek": RESULTS_DIR / "DeepSeek_Hybrid_reconciled.jsonl",
    "Llama": RESULTS_DIR / "Llama_Hybrid_reconciled.jsonl",
}


for model, path in HYBRID_FILES.items():

    print("\n" + "=" * 90)
    print(model)
    print("=" * 90)

    with open(path, "r", encoding="utf-8") as f:
        rows = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    total = len(rows)

    initial_tokens = [
        r.get("total_tokens", 0) or 0
        for r in rows
    ]

    initial_latency = [
        r.get("latency", 0) or 0
        for r in rows
    ]

    feedback_rows = [
        r for r in rows
        if r.get("was_corrected") is True
    ]

    feedback_tokens = [
        r.get("feedback_total_tokens", 0) or 0
        for r in feedback_rows
    ]

    feedback_latency = [
        r.get("feedback_latency", 0) or 0
        for r in feedback_rows
    ]

    # --------------------------------------------------------
    # Combined per-question cost
    # --------------------------------------------------------

    combined_tokens = []

    combined_latency = []

    for r in rows:

        initial = r.get("total_tokens", 0) or 0
        feedback = r.get("feedback_total_tokens", 0) or 0

        initial_time = r.get("latency", 0) or 0
        feedback_time = r.get("feedback_latency", 0) or 0

        combined_tokens.append(
            initial + feedback
        )

        combined_latency.append(
            initial_time + feedback_time
        )

    # --------------------------------------------------------
    # Recovery
    # --------------------------------------------------------

    recovered = [
        r for r in feedback_rows
        if r.get("reconciled_execution_accuracy") is True
    ]

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print(f"Questions: {total}")

    print(
        f"Feedback triggered: "
        f"{len(feedback_rows)} "
        f"({len(feedback_rows) / total * 100:.2f}%)"
    )

    print(
        f"Successful recoveries: "
        f"{len(recovered)}"
    )

    if feedback_rows:

        print(
            f"Feedback recovery rate: "
            f"{len(recovered) / len(feedback_rows) * 100:.2f}%"
        )

        print(
            f"Average feedback tokens "
            f"(triggered only): "
            f"{sum(feedback_tokens) / len(feedback_tokens):.2f}"
        )

        print(
            f"Average feedback latency "
            f"(triggered only): "
            f"{sum(feedback_latency) / len(feedback_latency):.3f} sec"
        )

        print(
            f"Total feedback tokens: "
            f"{sum(feedback_tokens)}"
        )

        print(
            f"Total feedback latency: "
            f"{sum(feedback_latency):.3f} sec"
        )

    print()

    print(
        f"Average initial tokens: "
        f"{sum(initial_tokens) / total:.2f}"
    )

    print(
        f"Average combined tokens: "
        f"{sum(combined_tokens) / total:.2f}"
    )

    print(
        f"Average initial latency: "
        f"{sum(initial_latency) / total:.3f} sec"
    )

    print(
        f"Average combined latency: "
        f"{sum(combined_latency) / total:.3f} sec"
    )

    # --------------------------------------------------------
    # Amortized feedback cost
    # --------------------------------------------------------

    total_feedback_tokens = sum(feedback_tokens)
    total_feedback_latency = sum(feedback_latency)

    print()

    print(
        f"Amortized feedback tokens/question: "
        f"{total_feedback_tokens / total:.2f}"
    )

    print(
        f"Amortized feedback latency/question: "
        f"{total_feedback_latency / total:.3f} sec"
    )