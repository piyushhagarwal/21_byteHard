# src/file2.py
from .file4 import square
def multiply(a, b):
    
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def complex_operation(a, b):
    
    product = multiply(a, b)
    squared_result = square(product)
    return squared_result
