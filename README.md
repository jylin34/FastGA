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
I make comparison between difference Genetic Algorithm implementation, FastGA, pure Python, and PyGAD, a well-known GA Python library, below is the result:

![Benchmark](/benchmarks/ga/ga_fastga_vs_python_vs_pygad_plot.png)

All three approaches successfully converged to highly similar solution, which is nearly optimal.

```
================================================================================
🏆 Best Solutions Found (at 10,000 generations)
Ideal Global Optimum: x=[1.0, 1.0], fitness=0.0
--------------------------------------------------------------------------------
FastGA       | x=[0.99974, 0.99949] | fitness=6.954409e-08
Pure Python  | x=[0.99996, 0.99991] | fitness=1.627944e-08
PyGAD        | x=[0.98507, 0.97028] | fitness=2.237055e-04
================================================================================
```

## Note
* pybind11 is esentially a pure C++ header only library
* Every python types are PyObject in CPython interpreter