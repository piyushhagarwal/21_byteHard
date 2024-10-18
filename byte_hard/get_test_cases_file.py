import os

def find_test_files_with_functions(test_folder, function_names):
    matching_files = []

    # Traverse the test folder recursively
    for root, dirs, files in os.walk(test_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Open and read each file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                try:
                    file_content = f.read()

                    # Check if any of the function names are present in the file
                    if any(func_name in file_content for func_name in function_names):
                        matching_files.append(file_path)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return matching_files

# if __name__ == "__main__":
#     # Example usage:
#     test_folder = "/Users/piyushagarwal/Downloads/Piyush/Mindspark/tests"
#     function_names = ["fibonacci", "merge_sort", "is_even"]

#     result = find_test_files_with_functions(test_folder, function_names)
#     print(result)
