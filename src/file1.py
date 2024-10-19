# complex_functions.py

import random
import string
import math
from functools import lru_cache

def factorial(n):
    """Compute the factorial of n using recursion."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """Return the nth Fibonacci number using memoization."""
    @lru_cache(maxsize=None)
    def fib(n):
        
        if n < 0:
            raise ValueError("Fibonacci is not defined for negative numbers.")
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    
    return fib(n)

def generate_random_string(length=10):
    """Generate a random string of specified length."""
    if length <= 0:
        raise ValueError("Length must be positive.")
    # Letters to choose from for generating random string
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def prime_factors(n):
    """Return the prime factors of a given number."""
    if n < 2:
        raise ValueError("Input must be an integer greater than 1.")
    factors = []
    for i in range(2, n + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    return factors

def bubble_sort(arr):
    """Sort an array using the bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def calculate_statistics(data):
    """Calculate mean, median, and mode of a list of numbers."""
    if not data:
        raise ValueError("Data must not be empty.")
    
    mean = sum(data) / len(data)
    sorted_data = sorted(data)
    mid = len(sorted_data) // 2
    median = (sorted_data[mid] + sorted_data[-mid - 1]) / 2 if len(data) % 2 == 0 else sorted_data[mid]
    
    mode = max(set(data), key=data.count)
    
    return {"mean": mean, "median": median, "mode": mode}

def merge_sort(arr):
    """Sort an array using the merge sort algorithm."""
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Checking with while
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr

def matrix_multiplication(A, B):
    """Multiply two matrices."""
    if len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions for multiplication.")
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def string_permutations(s):
    """Generate all permutations of a string."""
    if len(s) <= 1:
        return [s]
    permutations = []
    for i, char in enumerate(s):
        for perm in string_permutations(s[:i] + s[i+1:]):
            permutations.append(char + perm)
    return permutations

