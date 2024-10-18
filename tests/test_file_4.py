# tests/test_file4.py
import pytest
from ..src.file4 import square, cube, compute_square_and_cube

def test_square():
    assert square(3) == 9
    assert square(0) == 0

def test_cube():
    assert cube(3) == 27
    assert cube(0) == 0

def test_compute_square_and_cube():
    result = compute_square_and_cube(2, 3)
    assert result == (4, 27)
