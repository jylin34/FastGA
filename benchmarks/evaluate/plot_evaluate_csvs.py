import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
WITHOUT_BATCH_CSV = BASE_DIR / "evaluate_benchmark_results_without_batch.csv"
WITH_BATCH_CSV = BASE_DIR / "evaluate_benchmark_results_with_batch.csv"
OUTPUT_PNG = BASE_DIR / "evaluate_comparison_plot.png"


def load_results(csv_path: Path):
    generations = []
    total_seconds = []
    avg_ms = []

    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            generations.append(int(row["generations"]))
            total_seconds.append(float(row["total_seconds"]))
            avg_ms.append(float(row["avg_ms_per_evaluate"]))

    return generations, total_seconds, avg_ms


def main():
    if not WITHOUT_BATCH_CSV.exists():
        raise FileNotFoundError(f"Missing CSV: {WITHOUT_BATCH_CSV}")
    if not WITH_BATCH_CSV.exists():
        raise FileNotFoundError(f"Missing CSV: {WITH_BATCH_CSV}")

    gen_1, total_1, avg_1 = load_results(WITHOUT_BATCH_CSV)
    gen_2, total_2, avg_2 = load_results(WITH_BATCH_CSV)

    if gen_1 != gen_2:
        raise ValueError("The two CSV files have different generation steps and cannot be compared directly.")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].plot(gen_1, total_1, marker="o", linewidth=2, label="evaluate()")
    axes[0].plot(gen_2, total_2, marker="s", linewidth=2, label="batch_evaluate()")
    axes[0].set_title("Total Time")
    axes[0].set_xlabel("Number of Iterations (Generations)")
    axes[0].set_ylabel("Execution Time (Seconds)")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    axes[1].plot(gen_1, avg_1, marker="o", linewidth=2, label="evaluate()")
    axes[1].plot(gen_2, avg_2, marker="s", linewidth=2, label="batch_evaluate()")
    axes[1].set_title("Average Time per Call")
    axes[1].set_xlabel("Number of Iterations (Generations)")
    axes[1].set_ylabel("Milliseconds")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    axes[1].legend()

    fig.suptitle("evaluate() vs batch_evaluate() from CSV Results", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUTPUT_PNG, dpi=150)
    plt.close(fig)

    print(f"Saved plot to: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
