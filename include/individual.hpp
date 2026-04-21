#ifndef INDIVIDUAL_H
#define INDIVIDUAL_H
#pragma once // Prevent header file from multiple inclusion

#include <vector> 

class Individual { // Naming Convention: PascalCase
public:
    // Rule of Five
    Individual() = default; // Constructor
    Individual(Individual const &) = default; // Copy Constructor
    Individual(Individual &&) = default; // Move Constructor  
    Individual & operator=(Individual const &) = default; // Copy Assignment Operator
    Individual & operator=(Individual &&) = default; // Move Assignment Operator
    ~Individual() = default; // Destructor
    // Accessors
    std::vector<double> const & genes() const {return m_genes;} // genes getter 
    std::vector<double> & genes() {return m_genes;} // genes setter
    double const & fitness() const {return m_fitness;} // fitness getter
    double & fitness() {return m_fitness;} // fitness setter
    // There may be more function to add, or custom constructor / destructor
private:
    std::vector<double>  m_genes; // For private member data, we want a convention to distinguish them from other variables. Prefixing m_ is a common one. 
    double m_fitness = 0.0;
};

#endif
