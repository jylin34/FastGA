#ifndef GASOLVER_H
#define GASOLVER_H
#pragma once

#include "individual.hpp"
#include <vector>
#include <cstddef>
#include <functional>

class GASolver {
public:
    // Rule of Five
    GASolver() = default; // Constructor
    GASolver(size_t pop_size, size_t genome_size, double crossover_rate, double mutation_rate);
    GASolver(GASolver const &) = default; // Copy Constructor
    GASolver(GASolver &&) = default; // Move Constructor  
    GASolver & operator=(GASolver const &) = default; // Copy Assignment Operator
    GASolver & operator=(GASolver &&) = default; // Move Assignment Operator
    
    // Destructor
    ~GASolver() = default;

    void solve(int generations);
    const Individual& get_best_individual() const;

    size_t population_size() const { return m_pop_size; }
    double crossover_rate() const { return m_crossover_rate; }
    double mutation_rate() const { return m_mutation_rate; }
private:
    void evaluate();
    void selection();
    void crossover();
    void mutation();

    std::vector<Individual> m_population;
    double m_crossover_rate;
    double m_mutation_rate;
    size_t m_pop_size;

    std::function<double(const std::vector<double>&)> m_fitness_func;
};

#endif
