#include <gtest/gtest.h>
#include "ga_solver.hpp"
#include "individual.hpp"
#include <pybind11/embed.h> // For embedding Python
#include <pybind11/numpy.h>
#include <vector>

namespace py = pybind11;

TEST(GASolverEvaluateTest, CorrectlyCalculatesAndAssignsFitness) {
	py::scoped_interpreter guard{};

    try {
        py::module_ sys = py::module_::import("sys");
        
    } catch (const std::exception& e) {
        FAIL() << "環境路徑設定失敗: " << e.what();
    }
	py::dict globals = py::globals();
	py::exec(R"(
import numpy as np

def fitness_func(population):
    population = np.asarray(population, dtype=np.float64)
    return np.sum(population, axis=1)
)", globals, globals);

	py::function fitness_func = globals["fitness_func"].cast<py::function>();

	GASolver solver(2, 3, 0.8, 0.02);
	solver.set_fitness_func(fitness_func);

	solver.m_population[0].genes() = {1.0, 2.0, 3.0};
	solver.m_population[1].genes() = {4.0, 5.0, 6.0};

    solver.evaluate();

    EXPECT_DOUBLE_EQ(solver.m_population[0].fitness(), 6.0);
    EXPECT_DOUBLE_EQ(solver.m_population[1].fitness(), 15.0);
}




