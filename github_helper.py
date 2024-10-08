import os
import requests

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN', 'your_github_token')

def get_files_in_repo(api_url, subfolder=""):
    """
    Recursively get all file paths in a specific subfolder of a GitHub repository.
    """
    headers = {'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
    response = requests.get(api_url + subfolder, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching files from {subfolder}: {response.status_code}")
        return []

    files = []
    for item in response.json():
        if item['type'] == 'file':
            files.append(item)  # Save the file details (name, path, etc.)
        elif item['type'] == 'dir':
            files += get_files_in_repo(api_url, "/" + item['path'])

    return files
