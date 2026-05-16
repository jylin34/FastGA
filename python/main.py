import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build')))

import fastga

def sphere_function(genes: np.ndarray) -> float:
    return float(np.sum(genes**2))

def main():
    POPULATION_SIZE = 50
    GENOME_SIZE = 5  
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.02
    GENERATIONS = 100

    solver = fastga.GASolver(
        POPULATION_SIZE,
        GENOME_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE
    )

    solver.set_fitness_func(sphere_function)

    test_genes = np.arange(1, GENOME_SIZE + 1, dtype=np.float64)  # e.g., [1.0, 2.0, 3.0, 4.0, 5.0]
    fitness_value = solver.test_call_fitness(test_genes) # here is Deep Copy
    # C++ will create a vector<double> and make a copy of test_genes
    expected_fitness = np.sum(test_genes**2)
    assert fitness_value == expected_fitness, "Fitness bridge test failed!"
    print(fitness_value)

    # solver.solve(GENERATIONS)

    # best_individual = solver.get_best_individual()

if __name__ == "__main__":
    main()
