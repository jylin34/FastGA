#include "individual.hpp"
#include <algorithm>
#include <random>
#include <iostream>

// Constructor
Individual::Individual(int size) : m_fitness(0.0) {
    m_genes.resize(size);

    static std::random_device rd;
    static std::mt19937 gen(rd());
    // set to random variable between 0 ~ 1 (may adjust in the future)
    std::uniform_real_distribution<> dis(0.0, 1.0);
    for (double & gene : m_genes) {
        gene = dis(gen);
    }
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
