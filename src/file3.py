# src/file3.py
def is_even(number):
    return number % 2 == 0

def check_and_calculate(a, b):
    from .file5 import average
    numbers = [a, b]
    return average(numbers), is_even(a)
