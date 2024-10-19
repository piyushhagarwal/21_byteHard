from fastapi import FastAPI, Header, HTTPException
import requests
from pydantic import BaseModel, Field
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware


from byte_hard.get_changed_files import get_files_changed
from byte_hard.get_LLM_function_response import get_function_names
from byte_hard.get_test_cases_file import find_test_files_with_functions

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

GITHUB_API_URL = "https://api.github.com/repos/piyushhagarwal/Mindspark-24-25/commits"
token = "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"

@app.get("/commits")
def get_commits():
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch commits")

    commits = response.json()

    commit_data = [
        {"commit_id": commit["sha"], "commit_message": commit["commit"]["message"]}
        for commit in commits
    ]

    return commit_data

@app.get("/changed-files/")
def get_changed_files(commit_sha: str):
    try:
        changed_files = get_files_changed(commit_sha)
        return {"changed_files": changed_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define the structure for the inner patch and file_content
class FileData(BaseModel):
    patch: str
    file_content: str

# Define the overall request body structure
class ChangedFilesBody(BaseModel):
    changed_files: Dict[str, FileData]

@app.post("/process-changed-files/")
async def process_changed_files(body: ChangedFilesBody):
    # Extracting the changed files from the request body
    changed_files = body.changed_files
    
    function_names = []
    
    # changed_files is a dictionary with file names as keys and patch and file content as values
    for file_name, file_data in changed_files.items():
        # Get the function names from the LLM response
        function_names.extend(get_function_names(file_data.patch, file_data.file_content))  # Use dot notation here
        
    print(f"Function names extracted from the LLM response: {function_names}")

    # Find test files with the required functions
    test_files = find_test_files_with_functions("tests", function_names)
    
    # Prepare the list of JSON objects with test file paths and contents
    result = []
    for test_file in test_files:
        with open(test_file, 'r') as f:
            file_content = f.read()
        
        result.append({
            "test_file_path": test_file,
            "test_file_content": file_content
        })

    # Return the result as JSON
    return result

