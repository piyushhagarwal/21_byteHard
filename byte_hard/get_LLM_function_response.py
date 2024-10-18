import os
from together import Together

# Initialize the API client with your Together API key
client = Together(api_key='750bb823966720936d0334dc1ccfa3895dedde33ede71e0edf30028d6dae8249')

# Function to generate audit and remediation scripts from compliance JSON data for mac and linux
def get_function_names(updates, code_file_content, model_id="mistralai/Mistral-7B-Instruct-v0.3", max_tokens=1000, temperature=0.0):
    
    print("Preparing the prompt with the given updates and code file content...")

    # Define the prompt to be sent to the model
    prompt = f"""
      You are an expert in coding. You are given changes in code and the complete code file. 
      You have to give the function name in which the updates were made.
      Changes in file: {updates}
      Code file: {code_file_content}
      
      Give the output in structured json format
      ```json
        "function_names" : []
      ```
    """

    print(f"Sending the prompt to the model: {model_id}...")

    # Make the API request to generate the response
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    print("Received response from the model.")

    # Extract the generated output from the response
    output = response.choices[0].message.content
    print(f"Model output: {output}")
    
    return output

# if __name__ == "__main__":
#     updates = '''
#     @@ -17,6 +17,7 @@ def fibonacci(n):\n     """Return the nth Fibonacci number using memoization."""\n     @lru_cache(maxsize=None)\n     def fib(n):\n+        # Check for 0 condition\n         if n < 0:\n             raise ValueError("Fibonacci is not defined for negative numbers.")\n         if n <= 1:\n@@ -87,6 +88,7 @@ def merge_sort(arr):\n \n         i = j = k = 0\n \n+        # Checking with while\n         while i < len(left_half) and j < len(right_half):\n             if left_half[i] < right_half[j]:\n                 arr[k] = left_half[i]
#     '''
    
#     code_file_content = '''
#     # complex_functions.py\n\nimport random\nimport string\nimport math\nfrom functools import lru_cache\n\ndef factorial(n):\n    """Compute the factorial of n using recursion."""\n    if n < 0:\n        raise ValueError("Factorial is not defined for negative numbers.")\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\ndef fibonacci(n):\n    """Return the nth Fibonacci number using memoization."""\n    @lru_cache(maxsize=None)\n    def fib(n):\n        # Check for 0 condition\n        if n < 0:\n            raise ValueError("Fibonacci is not defined for negative numbers.")\n        if n <= 1:\n            return n\n        return fib(n - 1) + fib(n - 2)\n    \n    return fib(n)\n\ndef generate_random_string(length=10):\n    """Generate a random string of specified length."""\n    if length <= 0:\n        raise ValueError("Length must be positive.")\n    letters = string.ascii_letters\n    return \'\'.join(random.choice(letters) for _ in range(length))\n\ndef is_prime(num):\n    """Check if a number is prime."""\n    if num < 2:\n        return False\n    for i in range(2, int(math.sqrt(num)) + 1):\n        if num % i == 0:\n            return False\n    return True\n\ndef prime_factors(n):\n    """Return the prime factors of a given number."""\n    if n < 2:\n        raise ValueError("Input must be an integer greater than 1.")\n    factors = []\n    for i in range(2, n + 1):\n        while n % i == 0:\n            factors.append(i)\n            n //= i\n    return factors\n\ndef bubble_sort(arr):\n    """Sort an array using the bubble sort algorithm."""\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n\ndef calculate_statistics(data):\n    """Calculate mean, median, and mode of a list of numbers."""\n    if not data:\n        raise ValueError("Data must not be empty.")\n    \n    mean = sum(data) / len(data)\n    sorted_data = sorted(data)\n    mid = len(sorted_data) // 2\n    median = (sorted_data[mid] + sorted_data[-mid - 1]) / 2 if len(data) % 2 == 0 else sorted_data[mid]\n    \n    mode = max(set(data), key=data.count)\n    \n    return {"mean": mean, "median": median, "mode": mode}\n\ndef merge_sort(arr):\n    """Sort an array using the merge sort algorithm."""\n    if len(arr) > 1:\n        mid = len(arr) // 2\n        left_half = arr[:mid]\n        right_half = arr[mid:]\n\n        merge_sort(left_half)\n        merge_sort(right_half)\n\n        i = j = k = 0\n\n        # Checking with while\n        while i < len(left_half) and j < len(right_half):\n            if left_half[i] < right_half[j]:\n                arr[k] = left_half[i]\n                i += 1\n            else:\n                arr[k] = right_half[j]\n                j += 1\n            k += 1\n\n        while i < len(left_half):\n            arr[k] = left_half[i]\n            i += 1\n            k += 1\n\n        while j < len(right_half):\n            arr[k] = right_half[j]\n            j += 1\n            k += 1\n    return arr\n\ndef matrix_multiplication(A, B):\n    """Multiply two matrices."""\n    if len(A[0]) != len(B):\n        raise ValueError("Incompatible matrix dimensions for multiplication.")\n    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]\n    \n    for i in range(len(A)):\n        for j in range(len(B[0])):\n            for k in range(len(B)):\n                result[i][j] += A[i][k] * B[k][j]\n    return result\n\ndef string_permutations(s):\n    """Generate all permutations of a string."""\n    if len(s) <= 1:\n        return [s]\n    permutations = []\n    for i, char in enumerate(s):\n        for perm in string_permutations(s[:i] + s[i+1:]):\n            permutations.append(char + perm)\n    return permutations\n\n
#     '''
    
    
#     print(get_function_names(updates, code_file_content))