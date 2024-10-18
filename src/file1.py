# src/file1.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def math_operations(a, b):
    from .file2 import multiply
    from .file3 import is_even
    sum_value = add(a, b)
    product = multiply(a, b)
    even_check = is_even(sum_value)
    return sum_value, product, even_check
