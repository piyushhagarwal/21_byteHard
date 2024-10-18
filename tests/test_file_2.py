# tests/test_file2.py
import pytest
from ..src.file2 import multiply, divide, complex_operation

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5

    with pytest.raises(ValueError):
        divide(5, 0)

def test_complex_operation():
    result = complex_operation(2, 3)
    assert result == 36  # multiply(2, 3) == 6 -> square(6) == 36
