#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // 自動轉換 std::vector 和 python list
#include "individual.hpp"

namespace py = pybind11;

void init_individual(py::module &m) {
    py::class_<Individual>(m, "Individual")
        .def(py::init<int>(), py::arg("size"))

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

void init_population(py::module &m) {
    
}

PYBIND11_MODULE(fastga, m) {
    m.doc() = "FastGA: A high-performance Genetic Algorithm library.";
    
    init_individual(m);
    init_population(m);
}
