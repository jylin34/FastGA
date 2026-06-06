import csv
import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build')))
import fastga


def rosenbrock_function(population: np.ndarray) -> np.ndarray:
    g = np.asarray(population, dtype=np.float64)
    if g.ndim == 1:
        g = g.reshape(1, -1)

    if g.shape[1] < 2:
        x = g[:, 0] if g.shape[1] == 1 else np.zeros(g.shape[0], dtype=np.float64)
        return (1.0 - x) ** 2

    x_i = g[:, :-1]
    x_next = g[:, 1:]
    values = 100.0 * (x_next - x_i * x_i) ** 2 + (1.0 - x_i) ** 2
    return np.sum(values, axis=1)


def main() -> None:
    population_size = 100
    genome_size = 3
    crossover_rate = 0.5
    mutation_rate = 0.05
    upper_bound = 10.0
    lower_bound = -10.0

    iteration_steps = list(range(1000, 10001, 1000))

    solver = fastga.GASolver(
        population_size,
        genome_size,
        crossover_rate,
        mutation_rate,
        lower_bound,
        upper_bound,
    )
    solver.set_fitness_func(rosenbrock_function)

    evaluate_results = []
    batch_results = []

    print("-" * 80)
    print("Benchmarking GASolver.evaluate() vs GASolver.batch_evaluate()")
    print(f"Population Size: {population_size}, Genome Size: {genome_size}")
    print("Generation steps:", iteration_steps)
    print("-" * 80)

    for generations in iteration_steps:
        t0 = time.perf_counter()
        for _ in range(generations):
            solver.evaluate()
        elapsed = time.perf_counter() - t0
        avg_ms = elapsed * 1000.0 / generations
        evaluate_results.append((generations, elapsed, avg_ms))
        print(
            f"[evaluate]       generations={generations:5d}  total_time={elapsed:9.6f}s  avg_eval={avg_ms:9.6f}ms"
        )

        t0 = time.perf_counter()
        for _ in range(generations):
            solver.batch_evaluate()
        elapsed = time.perf_counter() - t0
        avg_ms = elapsed * 1000.0 / generations
        batch_results.append((generations, elapsed, avg_ms))
        print(
            f"[batch_evaluate] generations={generations:5d}  total_time={elapsed:9.6f}s  avg_eval={avg_ms:9.6f}ms"
        )

    output_csv = os.path.join(os.path.dirname(__file__), "evaluate_benchmark_results.csv")
    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["generations", "evaluate_total_seconds", "evaluate_avg_ms", "batch_total_seconds", "batch_avg_ms"])
        for idx, generations in enumerate(iteration_steps):
            ev = evaluate_results[idx]
            ba = batch_results[idx]
            writer.writerow([generations, ev[1], ev[2], ba[1], ba[2]])

    plt.figure(figsize=(10, 6))
    plt.plot(
        iteration_steps,
        [row[1] for row in evaluate_results],
        marker="o",
        linewidth=2,
        label="evaluate()",
    )
    plt.plot(
        iteration_steps,
        [row[1] for row in batch_results],
        marker="s",
        linewidth=2,
        label="batch_evaluate()",
    )
    plt.title("evaluate() vs batch_evaluate() Benchmark", fontsize=14, fontweight="bold")
    plt.xlabel("Number of Iterations (Generations)", fontsize=12)
    plt.ylabel("Execution Time (Seconds)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()

    output_png = os.path.join(os.path.dirname(__file__), "evaluate_benchmark_plot.png")
    plt.savefig(output_png)
    plt.close()

    print("-" * 80)
    print(f"Saved results to: {output_csv}")
    print(f"Saved plot to: {output_png}")
    print("-" * 80)


if __name__ == "__main__":
    main()