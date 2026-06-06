import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build')))

import fastga

# genome_size = 2
# -186.73
def shubert_function(population: np.ndarray) -> np.ndarray:
    # Accepts either a single 1D gene vector or a 2D population matrix.
    # Returns one fitness value per row.
    g = np.asarray(population, dtype=np.float64)
    if g.ndim == 1:
        g = g.reshape(1, -1)

    if g.shape[1] < 2:
        x1 = g[:, 0] if g.shape[1] == 1 else np.zeros(g.shape[0], dtype=np.float64)
        x2 = np.zeros(g.shape[0], dtype=np.float64)
    else:
        x1 = g[:, 0]
        x2 = g[:, 1]

    s1 = np.zeros(g.shape[0], dtype=np.float64)
    s2 = np.zeros(g.shape[0], dtype=np.float64)
    for i in range(1, 6):
        s1 += i * np.cos((i + 1) * x1 + i)
        s2 += i * np.cos((i + 1) * x2 + i)
    return s1 * s2

# genome_size = any
# accepts a 2D population matrix and returns one fitness value per row
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

def main():
    POPULATION_SIZE = 100
    GENOME_SIZE = 2
    CROSSOVER_RATE = 0.5
    MUTATION_RATE = 0.05
    GENERATIONS = 10000
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

    solver.set_fitness_func(shubert_function)
    solver.solve(GENERATIONS)

    best_individual = solver.get_best_individual()
    print("Best individual genes:", best_individual.genes)
    print("Best individual fitness:", best_individual.fitness)

if __name__ == "__main__":
    main()
