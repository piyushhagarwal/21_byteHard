# src/file4.py
from .file3 import check_and_calculate
def square(a):
    return a * a

def cube(a):
    # Using check_and_calculate from file3
    # Return the cube of a if a is even, otherwise return the square of a
    return a * a * check_and_calculate(a, a)[0]

def compute_square_and_cube(a, b):
    return square(a), cube(b)
