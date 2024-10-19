# src/file3.py
from .file5 import average
def is_even(number):
    return number % 2 == 0

def check_and_calculate(a, b):
    numbers = [a, b]
    return average(numbers), is_even(a)
