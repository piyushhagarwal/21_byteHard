# src/file5.py

from .file4 import cube
def average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list")
    
    # Calculate the average of the numbers
    return sum(numbers) / len(numbers)

def advanced_math_operations(a, b):
    cubed_value = cube(a*b)
    return cubed_value
