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


def test_ga_solver_evaluate_calls_fitness_for_each_individual():
	solver = fastga.GASolver(8, 4, 0.8, 0.02)
	calls = []

	def tracking_fitness(genes):
		genes_array = np.asarray(genes, dtype=np.float64)
		calls.append(genes_array)
		return np.sum(genes_array, axis=1)

	solver.set_fitness_func(tracking_fitness)
	solver.evaluate()

	assert len(calls) == 1
	assert calls[0].shape == (8, 4)


def test_ga_solver_mutation_changes_population_and_keeps_bounds():
	solver = fastga.GASolver(8, 4, 0.8, 1.0)

	def snapshot_population() -> np.ndarray:
		calls = []

		def tracking_fitness(genes):
			genes_array = np.asarray(genes, dtype=np.float64).copy()
			calls.append(genes_array)
			return float(np.sum(genes_array))

		solver.set_fitness_func(tracking_fitness)
		solver.evaluate()
		return np.vstack(calls)

	before = snapshot_population()
	solver.mutation()
	after = snapshot_population()

	assert before.shape == (8, 4)
	assert after.shape == (8, 4)
	assert np.any(np.abs(after - before) > 1e-12)


def test_ga_solver_selection_keeps_population_size_and_samples_existing_individuals():
	solver = fastga.GASolver(8, 4, 0.8, 0.02)

	def snapshot_population() -> np.ndarray:
		calls = []

		def tracking_fitness(genes):
			genes_array = np.asarray(genes, dtype=np.float64).copy()
			calls.append(genes_array)
			return float(np.sum(genes_array))

		solver.set_fitness_func(tracking_fitness)
		solver.evaluate()
		return np.vstack(calls)

	before = snapshot_population()
	solver.selection()
	after = snapshot_population()

	assert before.shape == (8, 4)
	assert after.shape == (8, 4)

	for selected in after:
		assert np.any(np.all(np.isclose(before, selected, atol=1e-12), axis=1))


def test_ga_solver_crossover_keeps_population_size_and_bounds():
	solver = fastga.GASolver(8, 4, 1.0, 0.02)

	def snapshot_population() -> np.ndarray:
		calls = []

		def tracking_fitness(genes):
			genes_array = np.asarray(genes, dtype=np.float64).copy()
			calls.append(genes_array)
			return float(np.sum(genes_array))

		solver.set_fitness_func(tracking_fitness)
		solver.evaluate()
		return np.vstack(calls)

	before = snapshot_population()
	solver.crossover()
	after = snapshot_population()

	assert before.shape == (8, 4)
	assert after.shape == (8, 4)
	assert np.any(np.abs(after - before) > 1e-12)
