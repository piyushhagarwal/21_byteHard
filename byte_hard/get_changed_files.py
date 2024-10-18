import requests
import json
import base64

def get_file_content(path):
    token = "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"
    url = f"https://api.github.com/repos/piyushhagarwal/Mindspark-24-25/contents/{path}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        content_data = response.json()
        # Decode Base64 content
        file_content = base64.b64decode(content_data['content']).decode('utf-8')
        return file_content
    else:
        return "Error in fetching file_content"


def extract_info(data):
    result = {}
    for item in data:
        filename = item['filename']
        
        result[filename] = {
            'changes': item['changes'],
            'file_content': get_file_content(filename)
        }
    return result

def get_files_changed(commit_sha):
    token = "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"
    url = f"https://api.github.com/repos/piyushhagarwal/Mindspark-24-25/commits/{commit_sha}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        output = response.json() # Return the list of commits
        output_dict = extract_info(output['files'])
        return output_dict
    else:
        return {"error": f"Failed to fetch commits. Status code: {response.status_code}"}


if __name__ == "__main__":
    sha = "6323b3a8e4637974186d1127ca3f7e0793c5e4bb"
    output = get_files_changed(sha)
    pretty_json = json.dumps(output, indent=4)
    print(pretty_json)
    
    
if __name__ == "__main__":
    commit_sha = sys.argv[1]
    changed_files = get_files_changed(commit_sha)
    
    print(f"Changed test files: {changed_files}")