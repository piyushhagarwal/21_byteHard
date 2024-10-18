# src/file2.py
def multiply(a, b):
    product = a * b
    return product

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def complex_operation(a, b):
    from .file4 import square
    product = multiply(a, b)
    squared_result = square(product)
    return squared_result
