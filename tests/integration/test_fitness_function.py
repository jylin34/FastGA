import pytest 
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build')))

import fastga

def test_fitness_function():
    solver = fastga.GASolver(10, 5, 0.8, 0.02)
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]

    def dummy_constant(genes):
        return 999.0

    solver.set_fitness_func(dummy_constant)
    res_const = solver.test_call_fitness(test_data)
    assert res_const == 999.0, f"常數測試失敗：預期 999.0，但得到 {res_const}"

    def dummy_length(genes):
        assert isinstance(genes, np.ndarray), "Zero-copy 失敗，底層未成功包裝成 NumPy 陣列！"
        return float(len(genes))

    solver.set_fitness_func(dummy_length)
    res_len = solver.test_call_fitness(test_data)
    assert res_len == 5.0, f"長度測試失敗：預期 5.0，但得到 {res_len}"

    def dummy_sum(genes):
        # 1.0 + 2.0 + 3.0 + 4.0 + 5.0 = 15.0
        return float(np.sum(genes))

    solver.set_fitness_func(dummy_sum)
    res_sum = solver.test_call_fitness(test_data)
    assert res_sum == 15.0, f"數值加總測試失敗：預期 15.0，但得到 {res_sum}"

    # --- 新增的、更複雜的測試案例 ---
    def complex_func(genes):
        # f(x, y) = x^2 + y^3 + 1
        x = genes[0]
        y = genes[1]
        return x**2 + y**3 + 1

    solver.set_fitness_func(complex_func)
    complex_test_data = [2.0, 3.0]
    res_complex = solver.test_call_fitness(complex_test_data)
    expected_complex = 32.0  # 2**2 + 3**3 + 1 = 4 + 27 + 1 = 32
    assert res_complex == expected_complex, f"複雜函式測試失敗：預期 {expected_complex}，但得到 {res_complex}"