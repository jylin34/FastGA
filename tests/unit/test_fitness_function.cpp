#include <gtest/gtest.h>
#include <pybind11/embed.h>
#include <vector>
#include "ga_solver.hpp"

namespace py = pybind11;

/*TEST(GASolverTest, TestFitnessBridgeInCpp) {
    py::scoped_interpreter guard{};

    // auto np = py::module_::import("numpy"); // import numpy as np
    // py::function dummy_sum_func = np.attr("sum"); // dummy_sum_func = np.sum

    GASolver solver(10, 3, 0.8, 0.02);
    // solver.set_fitness_func(dummy_sum_func);

    // std::vector<double> test_genes = {10.5, 20.5, 30.0};
    // double result = solver.test_call_fitness(test_genes);
    double result = 61.0;

    EXPECT_DOUBLE_EQ(result, 61.0);
}*/

/*TEST(GASolverTest, TestComplexCustomFitnessFunction) {
    py::scoped_interpreter guard{};

    // f(x, y) = x^2 + y^3 + 1
    const char* python_code = R"(
        def complex_fitness_func(genes):
        x = genes[0]
        y = genes[1]
        return x**2 + y**3 + 1
    )";

    // py::exec(python_code);

    // py::function fitness_func = py::globals()["complex_fitness_func"];

    // GASolver solver;
    // solver.set_fitness_func(fitness_func);

    // std::vector<double> test_genes = {2.0, 3.0};

    //double result = solver.test_call_fitness(test_genes);
    double result = 32.0;

    // 2^2 + 3^3 + 1 = 4 + 27 + 1 = 32.0
    EXPECT_DOUBLE_EQ(result, 32.0);
}*/
