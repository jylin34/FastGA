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
        sys.attr("path").attr("append")("../venv/lib/python3.14/site-packages"); 
        
    } catch (const std::exception& e) {
        FAIL() << "環境路徑設定失敗: " << e.what();
    }
	py::dict globals = py::globals();
	py::exec(R"(
def fitness_func(genes):
    return float(sum(genes))
)", globals, globals);

	py::function fitness_func = globals["fitness_func"].cast<py::function>();

	GASolver solver(2, 3, 0.8, 0.02);
	solver.set_fitness_func(fitness_func);

	solver.m_population[0].genes() = {1.0, 2.0, 3.0};
	solver.m_population[1].genes() = {4.0, 5.0, 6.0};

	{
        // py::gil_scoped_release 會主動把當前測試環境的 GIL 鎖放開。
        // 這會讓主執行緒處於「不持有鎖」的乾淨狀態。
        py::gil_scoped_release release;

        // 這裡面踩進 evaluate() 後，內部的 py::gil_scoped_acquire 就會完美地成功拿鎖、
        // 成功執行 py::array_t 零複製包裝、成功算完分數！
        solver.evaluate(); 
    }

	EXPECT_DOUBLE_EQ(solver.m_population[0].fitness(), 6.0);
	EXPECT_DOUBLE_EQ(solver.m_population[1].fitness(), 15.0);
}

