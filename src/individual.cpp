#include "individual.hpp"
#include <algorithm>
#include <random>
#include <iostream>

// Constructor
Individual::Individual(int size) : m_fitness(0.0) {
    m_genes.resize(size);

    static std::random_device rd;
    static std::mt19937 gen(rd());
    // Initialize genes from a normal distribution (mean=0, std=1)
    std::normal_distribution<> nd(0.0, 1.0);
    for (double & gene : m_genes) {
        gene = nd(gen);
    }
}

// Constructor with explicit uniform initialization in [lower, upper]
Individual::Individual(int size, double lower, double upper) : m_fitness(0.0) {
    m_genes.resize(size);

    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_real_distribution<> ud(lower, upper);
    for (double & gene : m_genes) {
        gene = ud(gen);
    }
}

Individual::Individual(const std::vector<double>& initial_genes) : m_genes(initial_genes), m_fitness(0.0) {
    // The member initializer list handles everything.
}

// Accessors Implementation
std::vector<double> const & Individual::genes() const { // genes getter
    return m_genes;
} 
std::vector<double> & Individual::genes() { // genes setter
    return m_genes;
} 
double const & Individual::fitness() const { // fitness getter
    return m_fitness;
} 
double & Individual::fitness() { // fitness setter
    return m_fitness;
}
