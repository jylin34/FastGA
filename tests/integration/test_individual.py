import pytest 
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../build')))

import fastga

def test_individual_constructor():
    size = 50
    ind = fastga.Individual(size)
    assert len(ind.genes) == size
    assert ind.fitness == 0.0

def test_individual_genes_read_write():
    size = 5
    ind = fastga.Individual(size)
    
    test_data = [1.1, 2.2, 3.3, 4.4, 5.5]
    ind.genes = test_data  # Call Setter
    
    assert ind.genes == test_data  # Call Getter 
    assert isinstance(ind.genes, list) # Make sure it is Python list

def test_individual_fitness_update():
    ind = fastga.Individual(10)
    new_score = 0.98765
    ind.fitness = new_score
    
    assert pytest.approx(ind.fitness) == new_score

def test_individual_large_scale():
    large_size = 10000
    ind = fastga.Individual(large_size)
    assert len(ind.genes) == large_size
