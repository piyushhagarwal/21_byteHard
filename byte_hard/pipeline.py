from get_changed_files import get_files_changed
from get_LLM_function_response import get_function_names
from get_test_cases_file import find_test_files_with_functions


def pipeline(commit_sha, test_cases_folder_path):
    # Get the files changed in the commit
    changed_files = get_files_changed(commit_sha)
    
    function_names = []
    
    # changed_files is a dictionary with file names as keys and patch and file content as values
    for file_name, file_data in changed_files.items():
        # Get the function names from the LLM response
        function_names.extend(get_function_names(file_data['patch'], file_data['file_content']))
        
        
    print(f"Function names extracted from the LLM response: {function_names}")

    # Find test files with the required functions
    test_files = find_test_files_with_functions(test_cases_folder_path, function_names)

    return test_files


if __name__ == "__main__":
    commit_sha = "ad8340b6e219d9018abbd2423c5464f75ddf9ec2"
    test_cases_folder_path = "/Users/piyushagarwal/Downloads/Piyush/Mindspark/tests"
    result = pipeline(commit_sha, test_cases_folder_path)
    print(result)