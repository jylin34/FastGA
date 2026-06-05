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
    Individual(int size);
    Individual(const std::vector<double>& initial_genes);
    
    // Destructor
    ~Individual() = default;

    // Accessors
    const std::vector<double>& genes() const; // genes getter 
    std::vector<double>& genes(); // genes setter
    const double& fitness() const; // fitness getter
    double& fitness(); // fitness setter
private:
    std::vector<double>  m_genes; // For private member data, we want a convention to distinguish them from other variables. Prefixing m_ is a common one. 
    double m_fitness = 0.0;
};

#endif
