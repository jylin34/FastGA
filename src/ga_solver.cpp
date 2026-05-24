#include "ga_solver.hpp"
#include "individual.hpp"
#include <vector>
#include <cstddef>
#include <pybind11/numpy.h>

namespace py = pybind11;

GASolver::GASolver(size_t pop_size, size_t genome_size, double crossover_rate, double mutation_rate)
    : m_crossover_rate(crossover_rate), 
      m_mutation_rate(mutation_rate), 
      m_pop_size(pop_size) {

    m_population.reserve(pop_size); // allocate memory for m_population in advance
    
    for (size_t i = 0; i < pop_size; i ++) {
        m_population.emplace_back(genome_size); // genome_size 會當作參數傳給 Individual
        // 用 emplace_back 可以達到 zero-copy ?
    }
}

void GASolver::solve(int generations) {
    for (int gen = 0; gen < generations; gen ++) {
        evaluate();
        selection();
        crossover();
        mutation();
    }
}

const Individual& GASolver::get_best_individual() const {
    return m_population[0];
}

double GASolver::test_call_fitness(const std::vector<double>& dummy_genes) {
    if (!m_fitness_func)    return -1.0;

    // numpy.ndarray float64
    // 告訴 NumPy 這個一維陣列的總長度（Shape）是多少。
    // Zero-Copy data() 會直接交出 C++ vector 在記憶體裡的 GPS 實體座標（指標 Pointer）。
    // 本質上建立了一個 Numpy object 這個物件內部的 data pointer 指向 c++ vector
    py::array_t<double> py_genes(dummy_genes.size(), dummy_genes.data());

    py::object raw_result = m_fitness_func(py_genes);
    return py::float_(raw_result).cast<double>();
}

// 把 m_population 裡每一個 Individual 丟進 fitness function 計算
// 可以做平行化
void GASolver::evaluate() {
    if (!m_fitness_func) {
        return; 
    }

    py::gil_scoped_acquire acquire; 

    for (size_t i = 0; i < m_population.size(); ++i) {
        Individual& ind = m_population[i];
        // 把 C++ vector 轉成 NumPy array，Zero-Copy
        py::array_t<double> py_genes(ind.genes().size(), ind.genes().data()); 
        py::object raw_result = m_fitness_func(py_genes);
        double score = py::float_(raw_result).cast<double>();
        ind.fitness() = score;
    }
}

// 從現有族群挑選出優秀個體，放進交配池中
// Roulette Wheel Selection / Tournament Selection
void GASolver::selection() {

}

// 開始交配
// 有不同交配方法
void GASolver::crossover() {

}

// 基因突變
// 有不同交配方法
// 可以平行化
void GASolver::mutation() {
    
}

// ========================= For Benchmark =========================
// =================================================================
// Scenario 2: Main loop in C++ with Zero-Copy Bridge
// =================================================================
double GASolver::benchmark_zero_copy_loop(const std::vector<double>& native_genes, int iterations) {
    if (!m_fitness_func) return -1.0;

    double total = 0.0;
    // The NumPy wrapper is constructed once outside the loop to map the pointer
    py::array_t<double> py_genes(native_genes.size(), native_genes.data());

    for (int i = 0; i < iterations; ++i) {
        py::object raw_result = m_fitness_func(py_genes);
        total += py::float_(raw_result).cast<double>();
    }
    return total;
}

// =================================================================
// Scenario 3: Main loop in C++ with Explicit Deep-Copy Per Iteration
// =================================================================
double GASolver::benchmark_deep_copy_loop(const std::vector<double>& native_genes, int iterations) {
    if (!m_fitness_func) return -1.0;

    double total = 0.0;
    size_t data_size = native_genes.size();

    for (int i = 0; i < iterations; ++i) {
        // Force a raw allocation and memory copy over the CPU heap on every iteration
        py::array_t<double> py_genes_copy(data_size);
        std::memcpy(py_genes_copy.mutable_data(), native_genes.data(), data_size * sizeof(double));

        py::object raw_result = m_fitness_func(py_genes_copy);
        total += py::float_(raw_result).cast<double>();
    }
    return total;
}
