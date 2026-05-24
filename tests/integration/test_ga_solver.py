import os
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "build"))

import fastga


def sphere_function(genes: np.ndarray) -> float:
	return float(np.sum(np.asarray(genes, dtype=np.float64) ** 2))


def test_ga_solver_constructor():
	solver = fastga.GASolver(8, 4, 0.8, 0.02)

	assert solver is not None


def test_ga_solver_calls_python_fitness_function():
	solver = fastga.GASolver(8, 5, 0.8, 0.02)
	solver.set_fitness_func(sphere_function)

	genes = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
	result = solver.test_call_fitness(genes)

	assert result == pytest.approx(55.0)


def test_ga_solver_returns_error_when_fitness_function_is_missing():
	solver = fastga.GASolver(8, 3, 0.8, 0.02)

	assert solver.test_call_fitness([1.0, 2.0, 3.0]) == pytest.approx(-1.0)
