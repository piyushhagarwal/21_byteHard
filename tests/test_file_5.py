# tests/test_file5.py
import pytest
from ..src.file5 import average, advanced_math_operations

def test_average():
    assert average([1, 2, 3]) == 2
    assert average([5, 5, 5]) == 5

    with pytest.raises(ValueError):
        average([])

def test_advanced_math_operations():
    result = advanced_math_operations(2, 3)
    assert result == (5, 6, True, 216)  # math_operations(2, 3) -> cube(6) == 216
