import csv
import math
import os
import random
import sys
import time
from typing import List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pygad

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build')))
import fastga


POPULATION_SIZE = 100
GENOME_SIZE = 2
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.05
UPPER_BOUND = 10.0
LOWER_BOUND = -10.0
GENERATION_STEPS = list(range(1000, 10001, 1000))


def rosenbrock_batch(population: np.ndarray) -> np.ndarray:
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


def rosenbrock_scalar(genes: Sequence[float]) -> float:
    if len(genes) < 2:
        x = float(genes[0]) if len(genes) == 1 else 0.0
        return float((1.0 - x) ** 2)

    total = 0.0
    for i in range(len(genes) - 1):
        x_i = float(genes[i])
        x_next = float(genes[i + 1])
        total += 100.0 * (x_next - x_i * x_i) ** 2 + (1.0 - x_i) ** 2
    return total

def pygad_fitness_func(ga_instance, solution, solution_idx):
    return -rosenbrock_scalar(solution)


class PurePythonGASolver:
    def __init__(
        self,
        population_size: int,
        genome_size: int,
        crossover_rate: float,
        mutation_rate: float,
        lower_bound: float,
        upper_bound: float,
        seed: int = 42,
    ) -> None:
        self.population_size = population_size
        self.genome_size = genome_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.rng = random.Random(seed)
        self.population = [
            [self.rng.uniform(lower_bound, upper_bound) for _ in range(genome_size)]
            for _ in range(population_size)
        ]
        self.fitness = [float("inf")] * population_size
        self.best_individual: List[float] | None = None
        self.best_fitness = float("inf")

    def evaluate(self) -> None:
        for idx, genes in enumerate(self.population):
            fitness = rosenbrock_scalar(genes)
            self.fitness[idx] = fitness
            if fitness < self.best_fitness:
                self.best_fitness = fitness
                self.best_individual = genes[:]

    def selection(self) -> None:
        max_fitness = max(self.fitness)
        weights = [max(0.0, max_fitness + 1.0 - value) for value in self.fitness]
        total_weight = sum(weights)

        new_population: List[List[float]] = []
        if total_weight <= 0.0:
            for _ in range(self.population_size):
                pick = self.rng.randrange(self.population_size)
                new_population.append(self.population[pick][:])
        else:
            cumulative = []
            running = 0.0
            for weight in weights:
                running += weight
                cumulative.append(running)

            for _ in range(self.population_size):
                target = self.rng.random() * total_weight
                chosen = 0
                while chosen < len(cumulative) and cumulative[chosen] < target:
                    chosen += 1
                if chosen >= self.population_size:
                    chosen = self.population_size - 1
                new_population.append(self.population[chosen][:])

        self.population = new_population

    def crossover(self) -> None:
        if self.crossover_rate <= 0.0 or not self.population:
            return

        alpha = 0.5
        new_population: List[List[float]] = []
        pair_limit = (len(self.population) // 2) * 2

        for i in range(0, pair_limit, 2):
            parent1 = self.population[i]
            parent2 = self.population[i + 1]

            if self.rng.random() > self.crossover_rate:
                new_population.append(parent1[:])
                new_population.append(parent2[:])
                continue

            child1 = []
            child2 = []
            for g1, g2 in zip(parent1, parent2):
                lower = min(g1, g2)
                upper = max(g1, g2)
                interval = upper - lower
                min_range = lower - alpha * interval
                max_range = upper + alpha * interval
                value1 = self.rng.uniform(min_range, max_range)
                value2 = self.rng.uniform(min_range, max_range)
                child1.append(min(max(value1, self.lower_bound), self.upper_bound))
                child2.append(min(max(value2, self.lower_bound), self.upper_bound))

            new_population.append(child1)
            new_population.append(child2)

        if len(self.population) % 2 == 1:
            new_population.append(self.population[-1][:])

        self.population = new_population

    def mutation(self) -> None:
        if self.mutation_rate <= 0.0:
            return

        sigma = 0.1
        for idx, genes in enumerate(self.population):
            for gene_idx in range(len(genes)):
                if self.rng.random() < self.mutation_rate:
                    new_value = genes[gene_idx] + self.rng.gauss(0.0, sigma)
                    genes[gene_idx] = min(max(new_value, self.lower_bound), self.upper_bound)

    def solve(self, generations: int) -> None:
        for _ in range(generations):
            self.evaluate()
            self.selection()
            self.crossover()
            self.mutation()

            if self.best_individual is not None and self.population:
                self.population[0] = self.best_individual[:]

        self.evaluate()


# 將 benchmark 函數修改為回傳 (耗時, 最佳解陣列, 最佳適應度)
def benchmark_fastga(generations: int) -> Tuple[float, List[float], float]:
    solver = fastga.GASolver(
        POPULATION_SIZE,
        GENOME_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        LOWER_BOUND,
        UPPER_BOUND,
    )
    solver.set_fitness_func(rosenbrock_batch)
    t0 = time.perf_counter()
    solver.solve(generations)
    dt = time.perf_counter() - t0
    
    best_ind = solver.get_best_individual()
    
    # 【關鍵修改】直接轉換為 Python list，這裡假設你有綁定 genes()
    # 如果你在 pybind11 中綁定了 genes()，直接呼叫它
    best_genes = list(best_ind.genes) 
    best_fitness = best_ind.fitness
    
    return dt, best_genes, best_fitness


def benchmark_python_ga(generations: int) -> Tuple[float, List[float], float]:
    solver = PurePythonGASolver(
        POPULATION_SIZE,
        GENOME_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        LOWER_BOUND,
        UPPER_BOUND,
    )
    t0 = time.perf_counter()
    solver.solve(generations)
    dt = time.perf_counter() - t0
    
    return dt, solver.best_individual, solver.best_fitness


def benchmark_pygad(generations: int) -> Tuple[float, List[float], float]:
    num_parents_mating = POPULATION_SIZE // 2

    ga_instance = pygad.GA(
        num_generations=generations,
        num_parents_mating=num_parents_mating,
        fitness_func=pygad_fitness_func,
        sol_per_pop=POPULATION_SIZE,
        num_genes=GENOME_SIZE,
        init_range_low=LOWER_BOUND,
        init_range_high=UPPER_BOUND,
        mutation_probability=MUTATION_RATE,
        crossover_probability=CROSSOVER_RATE,
        suppress_warnings=True
    )
    
    t0 = time.perf_counter()
    ga_instance.run()
    dt = time.perf_counter() - t0
    
    # 取得 PyGAD 的最佳解 (PyGAD 回傳的是 tuple: solution, solution_fitness, solution_idx)
    solution, solution_fitness, _ = ga_instance.best_solution()
    
    # 因為我們給 pygad_fitness_func 加上了負號，這裡要轉正回來
    real_fitness = -solution_fitness 
    return dt, list(solution), real_fitness


def main() -> None:
    rows = []

    print("-" * 80)
    print("Benchmarking fastga vs pure Python vs PyGAD on Rosenbrock function")
    print(f"Population Size: {POPULATION_SIZE}, Genome Size: {GENOME_SIZE}")
    print(f"Crossover Rate: {CROSSOVER_RATE}, Mutation Rate: {MUTATION_RATE}")
    print(f"Bounds: [{LOWER_BOUND}, {UPPER_BOUND}]")
    print(f"Generation steps: {GENERATION_STEPS}")
    print("-" * 80)

    # 用來儲存最後一次跑 10000 代的最佳解結果
    final_fastga_sol = None
    final_python_sol = None
    final_pygad_sol = None

    for generations in GENERATION_STEPS:
        fastga_time, f_genes, f_fit = benchmark_fastga(generations)
        python_time, p_genes, p_fit = benchmark_python_ga(generations)
        pygad_time, g_genes, g_fit = benchmark_pygad(generations)
        
        # 記錄最後一次迴圈的結果
        if generations == GENERATION_STEPS[-1]:
            final_fastga_sol = (f_genes, f_fit)
            final_python_sol = (p_genes, p_fit)
            final_pygad_sol = (g_genes, g_fit)
        
        rows.append(
            (
                generations,
                fastga_time,
                fastga_time * 1000.0 / generations,
                python_time,
                python_time * 1000.0 / generations,
                pygad_time,
                pygad_time * 1000.0 / generations,
            )
        )
        print(
            f"gen={generations:5d} | fastga={fastga_time:8.5f}s | python={python_time:8.5f}s | pygad={pygad_time:8.5f}s"
        )

    # --- 印出最後一次 (10,000 代) 的最佳解比較 ---
    print("\n" + "=" * 80)
    print("🏆 Best Solutions Found (at 10,000 generations)")
    print("Ideal Global Optimum: x=[1.0, 1.0], fitness=0.0")
    print("-" * 80)
    
    def print_sol(name: str, genes: List[float], fit: float):
        # 將基因列表格式化為小數點後 5 位
        genes_str = ", ".join([f"{g:.5f}" for g in genes])
        print(f"{name:12s} | x=[{genes_str}] | fitness={fit:.6e}")

    if final_fastga_sol: print_sol("FastGA", *final_fastga_sol)
    if final_python_sol: print_sol("Pure Python", *final_python_sol)
    if final_pygad_sol: print_sol("PyGAD", *final_pygad_sol)
    print("=" * 80 + "\n")

    csv_path = os.path.join(os.path.dirname(__file__), "ga_fastga_vs_python_vs_pygad_results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "generations",
                "fastga_total_seconds",
                "fastga_avg_ms_per_generation",
                "pure_python_total_seconds",
                "pure_python_avg_ms_per_generation",
                "pygad_total_seconds",
                "pygad_avg_ms_per_generation",
            ]
        )
        writer.writerows(rows)

    generations = [row[0] for row in rows]
    fastga_total = [row[1] for row in rows]
    pure_total = [row[3] for row in rows]
    pygad_total = [row[5] for row in rows]
    fastga_avg = [row[2] for row in rows]
    pure_avg = [row[4] for row in rows]
    pygad_avg = [row[6] for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    axes[0].plot(generations, fastga_total, marker="o", linewidth=2, label="fastga")
    axes[0].plot(generations, pygad_total, marker="^", linewidth=2, label="PyGAD")
    axes[0].plot(generations, pure_total, marker="s", linewidth=2, label="pure Python")
    axes[0].set_title("Total Solve Time")
    axes[0].set_xlabel("Generations")
    axes[0].set_ylabel("Seconds")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    axes[1].plot(generations, fastga_avg, marker="o", linewidth=2, label="fastga")
    axes[1].plot(generations, pygad_avg, marker="^", linewidth=2, label="PyGAD")
    axes[1].plot(generations, pure_avg, marker="s", linewidth=2, label="pure Python")
    axes[1].set_title("Average Time per Generation")
    axes[1].set_xlabel("Generations")
    axes[1].set_ylabel("Milliseconds")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    axes[1].legend()

    fig.suptitle("fastga vs PyGAD vs pure Python GA Benchmark on Rosenbrock", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    png_path = os.path.join(os.path.dirname(__file__), "ga_fastga_vs_python_vs_pygad_plot.png")
    fig.savefig(png_path, dpi=150)
    plt.close(fig)

    print("-" * 80)
    print(f"Saved CSV to: {csv_path}")
    print(f"Saved plot to: {png_path}")
    print("-" * 80)


if __name__ == "__main__":
    main()