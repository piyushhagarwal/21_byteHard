import requests
import json
import base64
import sys

def get_file_content(path):
    token = "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"
    url = f"https://api.github.com/repos/piyushhagarwal/Mindspark-24-25/contents/{path}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    print(f"Fetching file content for path: {path}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        content_data = response.json()
        print(f"File content fetched successfully for: {path}")
        # Decode Base64 content
        file_content = base64.b64decode(content_data['content']).decode('utf-8')
        return file_content
    else:
        print(f"Error in fetching file content for {path}, Status code: {response.status_code}")
        return None

def extract_info(data):
    print(f"Extracting patch info and file content for each changed file...")
    result = {}
    for item in data:
        filename = item['filename']
        
        print(f"Processing file: {filename}")
        file_content = get_file_content(filename)
        if file_content:
            result[filename] = {
                'patch': item['patch'],
                'file_content': file_content
            }
        else:
            print(f"Failed to fetch content for file: {filename}")
    return result

def get_files_changed(commit_sha):
    token = "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"
    url = f"https://api.github.com/repos/piyushhagarwal/Mindspark-24-25/commits/{commit_sha}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    print(f"Fetching changed files for commit: {commit_sha}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        output = response.json()  # Return the list of commits
        print(f"Successfully fetched changed files for commit: {commit_sha}")
        output_dict = extract_info(output['files'])
        return output_dict
    else:
        print(f"Error: Failed to fetch commit details. Status code: {response.status_code}")
        return {"error": f"Failed to fetch commit. Status code: {response.status_code}"}

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python script.py <commit_sha>")
#         sys.exit(1)

#     commit_sha = sys.argv[1]
#     print(f"Starting to process commit: {commit_sha}")

#     changed_files = get_files_changed(commit_sha)
    
#     print(f"Changed test files: {json.dumps(changed_files, indent=4)}")
#     print("Process completed.")
