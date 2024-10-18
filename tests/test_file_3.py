# tests/test_file3.py
import pytest
from ..src.file3 import is_even, check_and_calculate

def test_is_even():
    assert is_even(4) == True
    assert is_even(3) == False

def test_check_and_calculate():
    avg, is_even_check = check_and_calculate(4, 6)
    assert avg == 5
    assert is_even_check == True
