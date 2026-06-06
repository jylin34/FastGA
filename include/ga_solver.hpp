#ifndef GASOLVER_H
#define GASOLVER_H
#pragma once

#include "individual.hpp"
#include <vector>
#include <cstddef>
#include <functional>
#include <pybind11/pybind11.h>

#include <gtest/gtest_prod.h>

namespace py = pybind11;

class GASolver {
    FRIEND_TEST(GASolverEvaluateTest, CorrectlyCalculatesAndAssignsFitness);
public:
    // Rule of Five
    GASolver() = default; // Constructor
    GASolver(size_t pop_size, size_t genome_size, double crossover_rate, double mutation_rate);
    GASolver(size_t pop_size, size_t genome_size, double crossover_rate, double mutation_rate, double lower, double upper);
    GASolver(GASolver const &) = default; // Copy Constructor
    GASolver(GASolver &&) = default; // Move Constructor  
    GASolver & operator=(GASolver const &) = default; // Copy Assignment Operator
    GASolver & operator=(GASolver &&) = default; // Move Assignment Operator
    
    // Destructor
    ~GASolver() = default;

    void solve(int generations);
    const Individual& get_best_individual() const;
    void evaluate();
    void selection();
    void mutation();
    void crossover();

    void set_fitness_func(py::function func) {m_fitness_func = func;}
    double test_call_fitness(const std::vector<double>& dummy_genes);

    double benchmark_zero_copy_loop(const std::vector<double>& native_genes, int iterations);
    double benchmark_deep_copy_loop(const std::vector<double>& native_genes, int iterations);

    size_t population_size() const { return m_pop_size; }
    double crossover_rate() const { return m_crossover_rate; }
    double mutation_rate() const { return m_mutation_rate; }
private:
    // void evaluate();
    // void selection();
    // void mutation();
    // void crossover();

    std::vector<Individual> m_population;
    double m_crossover_rate;
    double m_mutation_rate;
    size_t m_pop_size;
    double m_lower_bound = -1.0;
    double m_upper_bound = 1.0;

    // Track the best individual seen across all generations (historical best)
    Individual m_best_individual;
    bool m_has_best = false;

    py::function m_fitness_func; // Smart pointer wrapping the user-defined Python fitness function
};

#endif
