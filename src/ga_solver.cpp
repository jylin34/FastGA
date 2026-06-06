#include "ga_solver.hpp"
#include "individual.hpp"
#include <vector>
#include <cstddef>
#include <pybind11/numpy.h>
#include <random>
#include <algorithm>
#include <cmath>
#include <limits>
#include <iostream>

namespace py = pybind11;

GASolver::GASolver(size_t pop_size, size_t genome_size, double crossover_rate, double mutation_rate)
    : GASolver(pop_size, genome_size, crossover_rate, mutation_rate, -1.0, 1.0) {}

GASolver::GASolver(size_t pop_size, size_t genome_size, double crossover_rate, double mutation_rate, double lower, double upper)
    : m_crossover_rate(crossover_rate), 
      m_mutation_rate(mutation_rate), 
      m_pop_size(pop_size),
      m_lower_bound(lower),
      m_upper_bound(upper)
    {
    m_population.reserve(pop_size); // allocate memory for m_population in advance
    for (size_t i = 0; i < pop_size; i ++) {
        m_population.emplace_back(genome_size, m_lower_bound, m_upper_bound);
    }
}

void GASolver::solve(int generations) {
    for (int gen = 0; gen < generations; gen ++) {
        batch_evaluate();
        // Print best individual found in this generation (minimization)
        if (!m_population.empty()) {
            double best_f = std::numeric_limits<double>::infinity();
            size_t best_idx = 0;
            for (size_t i = 0; i < m_population.size(); ++i) {
                double f = m_population[i].fitness();
                if (f < best_f) {
                    best_f = f;
                    best_idx = i;
                }
            }
            std::cout << "Gen " << gen << " best fitness=" << best_f << " genes=[";
            const auto &g = m_population[best_idx].genes();
            for (size_t k = 0; k < g.size(); ++k) {
                std::cout << g[k];
                if (k + 1 < g.size()) std::cout << ", ";
            }
            std::cout << "]\n";
            // Update historical best across all generations
            if (!m_has_best || best_f < m_best_individual.fitness()) {
                m_best_individual = m_population[best_idx];
                m_has_best = true;
            }
        }
        selection();
        crossover();
        mutation();

        if (m_has_best && !m_population.empty()) {
            m_population[0] = m_best_individual;
        }
    }
    batch_evaluate();  // Final evaluation after all generations

    // After final evaluation, ensure historical best reflects final population too
    if (!m_population.empty()) {
        double best_f = std::numeric_limits<double>::infinity();
        size_t best_idx = 0;
        for (size_t i = 0; i < m_population.size(); ++i) {
            double f = m_population[i].fitness();
            if (f < best_f) {
                best_f = f;
                best_idx = i;
            }
        }
        if (!m_has_best || best_f < m_best_individual.fitness()) {
            m_best_individual = m_population[best_idx];
            m_has_best = true;
        }
    }
}

const Individual& GASolver::get_best_individual() const {
    if (m_has_best) {
        return m_best_individual;
    }
    if (m_population.empty()) {
        throw std::runtime_error("Population is empty");
    }
    // Fallback: return current population best if historical best not initialized
    size_t best_idx = 0;
    double best_f = m_population[0].fitness();
    for (size_t i = 1; i < m_population.size(); ++i) {
        double f = m_population[i].fitness();
        if (f < best_f) {
            best_f = f;
            best_idx = i;
        }
    }
    return m_population[best_idx];
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
void GASolver::batch_evaluate() {
    if (!m_fitness_func) return; 

    py::gil_scoped_acquire acquire; 

    if (m_population.empty()) return;

    const size_t pop_size = m_population.size();
    const size_t genome_size = m_population.front().genes().size();

    py::array_t<double> py_population(
        { static_cast<py::ssize_t>(pop_size), static_cast<py::ssize_t>(genome_size) }
    );
    auto population_view = py_population.mutable_unchecked<2>();

    for (size_t i = 0; i < pop_size; ++i) {
        const std::vector<double>& native_genes = m_population[i].genes();
        for (size_t j = 0; j < genome_size; ++j) {
            population_view(i, j) = native_genes[j];
        }
    }

    py::object raw_result = m_fitness_func(py_population);
    py::array_t<double, py::array::c_style | py::array::forcecast> fitness_array =
        py::cast<py::array_t<double, py::array::c_style | py::array::forcecast>>(raw_result);

    if (fitness_array.ndim() != 1 || static_cast<size_t>(fitness_array.size()) != pop_size) {
        throw std::runtime_error("Batch fitness function must return a 1D array with one fitness value per individual");
    }

    auto fitness_view = fitness_array.unchecked<1>();

    for (size_t i = 0; i < pop_size; ++i) {
        m_population[i].fitness() = fitness_view(i);
    }
}

void GASolver::evaluate() {
    if (!m_fitness_func) return; 

    py::gil_scoped_acquire acquire; 

    for (size_t i = 0; i < m_population.size(); ++i) {
        Individual& ind = m_population[i];
        
        // 💡 1. 用 Reference 咬住記憶體，確保它在算完分數前絕對活著
        std::vector<double>& native_genes = ind.genes(); 
        
        // 💡 2. 建立 Zero-copy NumPy 陣列
        py::array_t<double> py_genes(
            { native_genes.size() },
            { sizeof(double) },
            native_genes.data(),
            py::handle()
        );

        py::object raw_result = m_fitness_func(py_genes);
        ind.fitness() = py::float_(raw_result).cast<double>();
    }
}

// 從現有族群挑選出優秀個體，放進交配池中
// Roulette Wheel Selection / Tournament Selection
void GASolver::selection() {
    if (m_population.empty()) return;

    static thread_local std::random_device rd;
    static thread_local std::mt19937 gen(rd());

    const size_t n = m_population.size();
    std::vector<double> weights;
    weights.reserve(n);

    double max_fitness = m_population[0].fitness();
    for (const Individual &ind : m_population) {
        max_fitness = std::max(max_fitness, ind.fitness());
    }

    // Reverse fitness for minimization: smaller fitness gets higher weight
    double total_weight = 0.0;
    for (const Individual &ind : m_population) {
        double w = max_fitness + 1.0 - ind.fitness();
        w = std::max(0.0, w);
        if (!std::isfinite(w)) w = 0.0;
        weights.push_back(w);
        total_weight += w;
    }

    std::vector<Individual> new_population;
    new_population.reserve(n);

    if (total_weight <= 0.0) {
        // Fallback: if all fitness are zero/invalid, sample uniformly.
        std::uniform_int_distribution<size_t> pick_uniform(0, n - 1);
        for (size_t i = 0; i < n; ++i) {
            new_population.push_back(m_population[pick_uniform(gen)]);
        }
    } else {
        std::discrete_distribution<size_t> pick(weights.begin(), weights.end());
        for (size_t i = 0; i < n; ++i) {
            new_population.push_back(m_population[pick(gen)]);
        }
    }

    m_population = std::move(new_population);
}

// 開始交配
// 有不同交配方法
void GASolver::crossover() {
    if (m_population.empty()) return;
    if (m_crossover_rate <= 0.0) return;

    static thread_local std::random_device rd;
    static thread_local std::mt19937 gen(rd());
    std::uniform_real_distribution<double> prob_dist(0.0, 1.0);

    constexpr double alpha = 0.5; // BLX-0.5

    std::vector<Individual> new_population;
    new_population.reserve(m_population.size());

    const size_t pop_size = m_population.size();
    const size_t last_pair_start = (pop_size / 2) * 2;

    // BLX generates values in an extended interval; do not clamp to [0,1]

    for (size_t i = 0; i + 1 < last_pair_start; i += 2) {
        const Individual &parent1 = m_population[i];
        const Individual &parent2 = m_population[i + 1];

        if (prob_dist(gen) > m_crossover_rate) {
            new_population.push_back(parent1);
            new_population.push_back(parent2);
            continue;
        }

        const std::vector<double> &genes1 = parent1.genes();
        const std::vector<double> &genes2 = parent2.genes();
        const size_t genome_size = std::min(genes1.size(), genes2.size());

        std::vector<double> child1_genes;
        std::vector<double> child2_genes;
        child1_genes.reserve(genome_size);
        child2_genes.reserve(genome_size);

        for (size_t j = 0; j < genome_size; ++j) {
            double g1 = genes1[j];
            double g2 = genes2[j];
            double lower = std::min(g1, g2);
            double upper = std::max(g1, g2);
            double interval = upper - lower;
            double min_range = lower - alpha * interval;
            double max_range = upper + alpha * interval;

            std::uniform_real_distribution<double> gene_dist(min_range, max_range);
            double cg1 = gene_dist(gen);
            double cg2 = gene_dist(gen);
            // Clamp to solver-specified bounds to avoid runaway values
            cg1 = std::clamp(cg1, m_lower_bound, m_upper_bound);
            cg2 = std::clamp(cg2, m_lower_bound, m_upper_bound);
            child1_genes.push_back(cg1);
            child2_genes.push_back(cg2);
        }

        Individual child1(child1_genes);
        Individual child2(child2_genes);
        // Invalidate fitness so evaluate() will recalculate
        child1.fitness() = -1.0;
        child2.fitness() = -1.0;
        new_population.push_back(child1);
        new_population.push_back(child2);
    }

    // If population size is odd, keep the last individual as-is.
    if (pop_size % 2 == 1) {
        new_population.push_back(m_population.back());
    }

    m_population = std::move(new_population);
}

// 基因突變
// 有不同交配方法
// 可以平行化
void GASolver::mutation() {
    if (m_mutation_rate <= 0.0) return;

    static thread_local std::random_device rd;
    static thread_local std::mt19937 gen(rd());
    std::uniform_real_distribution<double> prob_dist(0.0, 1.0);
    // Gaussian perturbation: mean=0, stddev controls mutation magnitude
    const double sigma = 0.1; // default standard deviation for Gaussian mutation
    std::normal_distribution<double> normal_dist(0.0, sigma);

    for (size_t i = 0; i < m_population.size(); ++i) {
        Individual &ind = m_population[i];
        std::vector<double> &genes = ind.genes();
        for (size_t j = 0; j < genes.size(); ++j) {
            if (prob_dist(gen) < m_mutation_rate) {
                double new_val = genes[j] + normal_dist(gen);
                // Clamp mutated gene to bounds
                genes[j] = std::clamp(new_val, m_lower_bound, m_upper_bound);
            }
        }
    }
    
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
