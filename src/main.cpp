#include "individual.hpp"
#include <vector>
#include <iostream>

int main() {
    Individual ind(10);
    std::cout << "Individual created with 10 genes: " << std::endl;
    const std::vector<double> & genes = ind.genes();
    for (const double & gene : genes) {
        std::cout << gene << " ";
    }
    std::cout << std::endl;
    return 0;
}
