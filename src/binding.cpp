#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // 自動轉換 std::vector 和 python list
#include "individual.hpp"
#include "ga_solver.hpp"

namespace py = pybind11;

void init_individual(pybind11::module &m) {
    py::class_<Individual>(m, "Individual")
        .def(py::init<int>(), py::arg("size"))
        .def(py::init<int, double, double>(), py::arg("size"), py::arg("lower"), py::arg("upper"))

        .def_property("genes",
            // Getter
            static_cast<std::vector<double> const& (Individual::*)() const>(&Individual::genes),
            // Setter
            [](Individual &ind, const std::vector<double> &new_genes) {
                ind.genes() = new_genes;
            }
        )

        .def_property("fitness",
            // Getter
            static_cast<double const& (Individual::*)() const>(&Individual::fitness),
            // Setter
            [](Individual &ind, double new_fitness) {
                ind.fitness() = new_fitness;
            }
        );
}

void init_population(pybind11::module &m) {
    
}

void init_ga_solver(pybind11::module &m) {
    py::class_<GASolver>(m, "GASolver")
        .def(py::init<size_t, size_t, double, double>()) 
        .def(py::init<size_t, size_t, double, double, double, double>(), py::arg("pop_size"), py::arg("genome_size"), py::arg("crossover_rate"), py::arg("mutation_rate"), py::arg("lower"), py::arg("upper"))
        .def("solve", &GASolver::solve)
        .def("get_best_individual", &GASolver::get_best_individual, py::return_value_policy::reference_internal)
        .def("set_fitness_func", &GASolver::set_fitness_func)
        .def("evaluate", &GASolver::evaluate)
        .def("selection", &GASolver::selection)
        .def("crossover", &GASolver::crossover)
        .def("mutation", &GASolver::mutation)
        .def("test_call_fitness", &GASolver::test_call_fitness);
}

PYBIND11_MODULE(fastga, m) {
    m.doc() = "FastGA: A high-performance Genetic Algorithm library.";
    
    init_individual(m);
    init_population(m);
    init_ga_solver(m);
}
