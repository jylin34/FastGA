import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build')))

import fastga

# genome_size = 2
# -186.73
def shubert_function(genes: np.ndarray) -> float:
    # f(x) = (sum_{i=1..5} i * cos((i+1)*x1 + i)) * (sum_{i=1..5} i * cos((i+1)*x2 + i))
    # Use first two genes as x1 and x2 (pad with 0 if missing)
    g = np.asarray(genes, dtype=np.float64)
    x1 = float(g[0]) if g.size > 0 else 0.0
    x2 = float(g[1]) if g.size > 1 else 0.0
    s1 = 0.0
    s2 = 0.0
    for i in range(1, 6):
        s1 += i * np.cos((i + 1) * x1 + i)
        s2 += i * np.cos((i + 1) * x2 + i)
    return float(s1 * s2)

# genome_size = any
# 0, all 1
def rosenbrock_function(genes: np.ndarray) -> float:
    g = np.asarray(genes, dtype=np.float64)
    if g.size < 2:
        x = float(g[0]) if g.size == 1 else 0.0
        return float((1.0 - x) ** 2)

    total = 0.0
    for i in range(g.size - 1):
        x_i = float(g[i])
        x_next = float(g[i + 1])
        total += 100.0 * (x_next - x_i * x_i) ** 2 + (1.0 - x_i) ** 2
    return float(total)

def main():
    POPULATION_SIZE = 200
    GENOME_SIZE = 3
    CROSSOVER_RATE = 0.5
    MUTATION_RATE = 0.05
    GENERATIONS = 8000
    UPPER_BOUND = 10.0
    LOWER_BOUND = -10.0

    solver = fastga.GASolver(
        POPULATION_SIZE,
        GENOME_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        LOWER_BOUND,
        UPPER_BOUND
    )

    solver.set_fitness_func(rosenbrock_function)
    solver.solve(GENERATIONS)

    best_individual = solver.get_best_individual()
    print("Best individual genes:", best_individual.genes)
    print("Best individual fitness:", best_individual.fitness)

if __name__ == "__main__":
    main()
