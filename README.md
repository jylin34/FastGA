# FastGA
FastGA is a high-performance C++ genetic algorithm (GA) library with Python bindings, specifically optimized for global optimization problems represented by 1D double-precision vectors.

# Build & Test
```bash=
git clone https://github.com/jylin34/FastGA
cd FastGA
mkdir build && cd build
cmake ..
cmake --build .
ctest
```

# Quick Start
```bash=
cd python
python main.py
```

```py
import numpy
import fastga

# 1. Define your custom fitness function (must accept a NumPy array and return a float)
def sphere_function(genes: np.ndarray) -> float:
    return float(np.sum(genes**2))

def main():
    # 2. Configure the Genetic Algorithm parameters
    POPULATION_SIZE = 50
    GENOME_SIZE = 5  
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.02
    LOWER_BOUND = -5.12
    UPPER_BOUND = 5.12
    GENERATIONS = 100

    # 3. Initialize the Solver
    solver = fastga.GASolver(
        POPULATION_SIZE,
        GENOME_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        LOWER_BOUND,
        UPPER_BOUND
    )

    # 4. Attach the fitness function
    solver.set_fitness_func(sphere_function)

    # 5. Run the evolution
    solver.solve(GENERATIONS)

    # 6. Retrieve the global best result
    best_individual = solver.get_best_individual()
    print(f"Best Genes: {best_individual.genes}")
    print(f"Best Fitness: {best_individual.fitness}")

if __name__ == "__main__":
    main()
```

# Benchmark

## Note
* pybind11 is esentially a pure C++ header only library
* Every python types are PyObject in CPython interpreter