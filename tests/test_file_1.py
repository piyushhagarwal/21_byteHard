# test_complex_functions.py
import pytest
from src.file1 import (
    factorial, fibonacci, generate_random_string, is_prime,
    prime_factors, bubble_sort, calculate_statistics, merge_sort,
    matrix_multiplication, string_permutations
)

def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    with pytest.raises(ValueError):
        factorial(-1)

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(6) == 8
    with pytest.raises(ValueError):
        fibonacci(-1)

def test_generate_random_string():
    result = generate_random_string(10)
    assert len(result) == 10
    assert isinstance(result, str)
    with pytest.raises(ValueError):
        generate_random_string(0)

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(17) is True
    assert is_prime(1) is False

def test_prime_factors():
    assert prime_factors(28) == [2, 2, 7]
    assert prime_factors(29) == [29]
    with pytest.raises(ValueError):
        prime_factors(1)

def test_bubble_sort():
    assert bubble_sort([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]
    assert bubble_sort([]) == []
    assert bubble_sort([1]) == [1]

def test_calculate_statistics():
    data = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9]
    stats = calculate_statistics(data)
    assert stats['mean'] == pytest.approx(5)
    assert stats['median'] == 5
    assert stats['mode'] == 5
    with pytest.raises(ValueError):
        calculate_statistics([])

def test_merge_sort():
    assert merge_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]

def test_matrix_multiplication():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    assert matrix_multiplication(A, B) == [[19, 22], [43, 50]]
    with pytest.raises(ValueError):
        matrix_multiplication([[1, 2]], [[1, 2]])

def test_string_permutations():
    assert set(string_permutations("abc")) == set(['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    assert string_permutations("a") == ["a"]

if __name__ == "__main__":
    pytest.main()
