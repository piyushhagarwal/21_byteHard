import os

def extract_called_functions(file_path, function_names):
    """Extracts functions that are called from a given file."""
    called_functions = set()
    
    with open(file_path, "r") as file:
        content = file.read()
        for func in function_names:
            if func in content:
                lines = content.splitlines()
                for line in lines:
                    if func in line and "(" in line and ")" in line:
                        # Basic heuristic to find function calls: name followed by ()
                        called_functions.add(func)
    
    return called_functions

def search_function_calls(dir_path, initial_function_names):
    """Searches for files where any of the given function names are called, iteratively."""
    visited_files = set()
    function_names = set(initial_function_names)  # Functions to search for
    calling_files = []
    
    while function_names:
        new_function_names = set()

        for root, _, files in os.walk(dir_path):
            for filename in files:
                if filename.endswith(".py"):
                    file_path = os.path.join(root, filename)
                    
                    # Avoid visiting the same file multiple times
                    if file_path in visited_files:
                        continue
                    
                    # Extract called functions in this file
                    called_funcs = extract_called_functions(file_path, function_names)
                    if called_funcs:
                        calling_files.append(file_path)
                        new_function_names.update(called_funcs)
                        visited_files.add(file_path)
        
        # Stop if no new functions are found
        if not new_function_names.difference(function_names):
            break
        
        # Update function names to search for in the next iteration
        function_names = new_function_names

    return calling_files

if __name__ == "__main__":
    dir_path = "/Users/piyushagarwal/Downloads/Piyush/Mindspark/src"
    function_names = ["average"]  # Initial function to search for
    result = search_function_calls(dir_path, function_names)
    print(result)
