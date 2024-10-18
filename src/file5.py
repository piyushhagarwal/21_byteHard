# src/file5.py
def average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list")
    
    # Calculate the average of the numbers
    return sum(numbers) / len(numbers)

def advanced_math_operations(a, b):
    from .file1 import math_operations
    from .file4 import cube
    sum_value, product, even_check = math_operations(a, b)
    cubed_value = cube(product)
    return sum_value, product, even_check, cubed_value
