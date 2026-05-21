import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# Ensure the script can locate the built fastga module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build')))
import fastga

# Experiment 1 Target: Vectorized using optimized C-extensions (NumPy)
def sphere_function(genes: np.ndarray) -> float:
    return float(np.sum(genes**2))

# Experiment 2 Target: Iterative using standard CPython loops (Pure Python)
def pure_python_fitness(genes) -> float:
    total = 0.0
    for g in genes:  
        total += g ** 2
    return total

def main():
    # Configuration parameters
    POPULATION_SIZE = 50
    GENOME_SIZE = 10000     
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.02
    
    # Define the exact loop iteration steps requested
    iteration_steps = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                       10000]

    solver = fastga.GASolver(
        POPULATION_SIZE,
        GENOME_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE
    )

    # Prepare input data
    test_genes_np = np.arange(1, GENOME_SIZE + 1, dtype=np.float64)
    zero_copy_view = test_genes_np.view()

    # Data structures to store timing results for plotting
    exp1_g1_times, exp1_g2_times, exp1_g3_times = [], [], []
    exp2_g1_times, exp2_g2_times, exp2_g3_times = [], [], []

    print("-" * 80)
    print(f"Starting Multi-Step Benchmark (Genome Size: {GENOME_SIZE:,})")
    print("-" * 80)

    for iterations in iteration_steps:
        print(f"Running benchmarks for {iterations} iterations...")

        # -----------------------------------------------------------------
        # EXPERIMENT 1: NumPy Vectorized Fitness Function
        # -----------------------------------------------------------------
        solver.set_fitness_func(sphere_function)
        
        # Group 1: Pure Python Loop Baseline
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = sphere_function(test_genes_np)
        exp1_g1_times.append(time.perf_counter() - t0)

        # Group 2: Simulated C++ Zero-Copy Pipeline
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = sphere_function(zero_copy_view)
        exp1_g2_times.append(time.perf_counter() - t0)

        # Group 3: C++ Bridge with Implicit Deep Copy
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = solver.test_call_fitness(test_genes_np)  
        exp1_g3_times.append(time.perf_counter() - t0)

        # -----------------------------------------------------------------
        # EXPERIMENT 2: Pure Python Iterative Fitness Function
        # -----------------------------------------------------------------
        solver.set_fitness_func(pure_python_fitness)
        
        # Group 1: Pure Python Loop Baseline
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = pure_python_fitness(test_genes_np)
        exp2_g1_times.append(time.perf_counter() - t0)

        # Group 2: Simulated C++ Zero-Copy Pipeline
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = pure_python_fitness(zero_copy_view)
        exp2_g2_times.append(time.perf_counter() - t0)

        # Group 3: C++ Bridge with Implicit Deep Copy
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = solver.test_call_fitness(test_genes_np)  
        exp2_g3_times.append(time.perf_counter() - t0)

    print("-" * 80)
    print("Benchmark completed. Generating plots...")
    print("-" * 80)

    # =================================================================
    # PLOTTING CHART 1: NumPy Vectorized Fitness Function
    # =================================================================
    plt.figure(figsize=(10, 6))
    plt.plot(iteration_steps, exp1_g1_times, label="Group 1 (Pure Python Loop)", marker='o', linewidth=2)
    plt.plot(iteration_steps, exp1_g2_times, label="Group 2 (C++ Zero-Copy)", marker='s', linewidth=2)
    plt.plot(iteration_steps, exp1_g3_times, label="Group 3 (C++ Deep Copy)", marker='^', linewidth=2)
    
    plt.title("Experiment 1: NumPy Vectorized Fitness Function Performance", fontsize=14, fontweight='bold')
    plt.xlabel("Number of Iterations (Loops)", fontsize=12)
    plt.ylabel("Execution Time (Seconds)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    chart1_filename = "benchmark_numpy_fitness.png"
    plt.savefig(chart1_filename)
    print(f"Saved Chart 1: {chart1_filename}")
    plt.close()

    # =================================================================
    # PLOTTING CHART 2: Pure Python Iterative Fitness Function
    # =================================================================
    plt.figure(figsize=(10, 6))
    plt.plot(iteration_steps, exp2_g1_times, label="Group 1 (Pure Python Loop)", marker='o', linewidth=2)
    plt.plot(iteration_steps, exp2_g2_times, label="Group 2 (C++ Zero-Copy)", marker='s', linewidth=2)
    plt.plot(iteration_steps, exp2_g3_times, label="Group 3 (C++ Deep Copy)", marker='^', linewidth=2)
    
    plt.title("Experiment 2: Pure Python Iterative Fitness Function Performance", fontsize=14, fontweight='bold')
    plt.xlabel("Number of Iterations (Loops)", fontsize=12)
    plt.ylabel("Execution Time (Seconds)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    chart2_filename = "benchmark_pure_python_fitness.png"
    plt.savefig(chart2_filename)
    print(f"Saved Chart 2: {chart2_filename}")
    plt.close()

    print("-" * 80)
    print("All charts generated successfully.")
    print("-" * 80)

if __name__ == "__main__":
    main()
