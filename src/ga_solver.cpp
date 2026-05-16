#include "ga_solver.hpp"
#include "individual.hpp"
#include <vector>
#include <cstddef>

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

// 把 m_population 裡每一個 Individual 丟進 fitness function 計算
// 可以做平行化
void GASolver::evaluate() {
    
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
