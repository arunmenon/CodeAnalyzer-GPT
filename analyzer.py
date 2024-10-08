import os
import requests
import time
from multiprocessing import Process


# Set your GitHub and OpenAI API tokens as environment variables for security
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN', 'your_github_token')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
REPO_OWNER = 'vllm-project'
REPO_NAME = 'vllm'

# Base GitHub API URL for repository content
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents"

# Define output folder where analyses will be saved
OUTPUT_FOLDER = "analysis_output"
FINAL_WRITEUP_FILE = "final_writeup.txt"


def load_user_prompt_prefix(config_file='config.txt'):
    """Loads the user prompt prefix from a config file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found.")
    
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('USER_PROMPT_PREFIX'):
                return line.split('=', 1)[1].strip()  # Strip any extra spaces or newlines
    
    raise ValueError("USER_PROMPT_PREFIX not found in the config file.")

# Load the prompt prefix from the config file
USER_PROMPT_PREFIX = load_user_prompt_prefix()

def get_files_in_repo(api_url, subfolder=""):
    """
    Recursively get all file paths in a specific subfolder of a GitHub repository.
    If subfolder is empty, the root folder is scanned.
    """
    headers = {'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
    response = requests.get(api_url + subfolder, headers=headers)

    # Check for errors
    if response.status_code != 200:
        print(f"Error fetching files from {subfolder}: {response.status_code}")
        return []

    files = []
    for item in response.json():
        if item['type'] == 'file':
            files.append(item)  # Save the file details (name, path, etc.)
        elif item['type'] == 'dir':
            # Recursively fetch files from directories
            files += get_files_in_repo(api_url, "/" + item['path'])

    return files

def send_file_to_gpt4(file_url, user_prompt_prefix):
    """Send file content to GPT-4 for analysis."""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    # Fetch the file content
    file_content = requests.get(file_url).text

    # GPT-4 request body with customizable prompt prefix
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{user_prompt_prefix}\n\n{file_content}"}
        ]
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )

    # Check for OpenAI API errors
    if response.status_code != 200:
        print(f"Error analyzing file {file_url}: {response.status_code}")
        return None

    # Get the GPT-4 analysis result
    result = response.json()
    return result['choices'][0]['message']['content']

def save_analysis(file_data, analysis):
    """
    Save the GPT-4 analysis to a file, maintaining the directory structure.
    file_data: contains the 'name' and 'path' of the file from GitHub.
    analysis: the analysis result to be saved.
    """
    # Create a path that mirrors the repo structure within the output folder
    relative_path = file_data['path']
    analysis_file_path = os.path.join(OUTPUT_FOLDER, relative_path + ".analysis.txt")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(analysis_file_path), exist_ok=True)

    # Write the analysis to the file
    with open(analysis_file_path, 'w', encoding='utf-8') as analysis_file:
        analysis_file.write(analysis)

def generate_writeup_from_analysis():
    """Reads all completed analysis files and generates a final writeup."""
    all_analyses = []

    # Traverse the analysis folder and collect all analyses
    for root, _, files in os.walk(OUTPUT_FOLDER):
        for file in files:
            if file.endswith(".analysis.txt"):
                analysis_path = os.path.join(root, file)
                with open(analysis_path, 'r', encoding='utf-8') as analysis_file:
                    content = analysis_file.read()
                    all_analyses.append(content)
    
    # Combine all analyses into one prompt for GPT-4
    combined_analysis = "\n\n".join(all_analyses)
    
    # Send the combined analysis to GPT-4 for summarization
    print("Sending combined analysis to GPT-4 for writeup generation...")
    final_writeup = send_to_gpt4_for_writeup(combined_analysis)
    
    # Save the final writeup
    if final_writeup:
        with open(FINAL_WRITEUP_FILE, 'w', encoding='utf-8') as writeup_file:
            writeup_file.write(final_writeup)
        print(f"Final writeup saved to {FINAL_WRITEUP_FILE}.")
    else:
        print("Failed to generate final writeup.")


def send_to_gpt4_for_writeup(content):
    """Send analysis content to GPT-4 for summarization."""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    # GPT-4 request body
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please generate a detailed writeup based on the following analyses:\n\n{content}"}
        ]
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )

    # Check for OpenAI API errors
    if response.status_code != 200:
        print(f"Error analyzing content: {response.status_code}")
        return None

    # Get the GPT-4 result
    result = response.json()
    return result['choices'][0]['message']['content']

def monitor_and_generate_writeup(expected_analysis_files):
    """Monitors the analysis folder and triggers writeup generation once all analysis files are complete."""
    
    print(f"Expecting {len(expected_analysis_files)} analysis files...")
    
    while True:
        # Get the list of current analysis files
        completed_analysis_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(OUTPUT_FOLDER)
            for file in files if file.endswith(".analysis.txt")
        ]
        
        # Check if the number of completed files matches the expected number
        if len(completed_analysis_files) >= len(expected_analysis_files):
            print(f"All {len(completed_analysis_files)} analysis files are completed. Generating writeup...")
            generate_writeup_from_analysis(completed_analysis_files)
            break
        else:
            print(f"Only {len(completed_analysis_files)} of {len(expected_analysis_files)} files completed. Waiting...")
            time.sleep(10)  # Wait for 10 seconds before checking again

def generate_writeup_from_analysis(completed_analysis_files):
    """Reads completed analysis files and generates a final writeup."""
    
    all_analyses = []
    
    for analysis_file_path in completed_analysis_files:
        with open(analysis_file_path, 'r', encoding='utf-8') as analysis_file:
            content = analysis_file.read()
            all_analyses.append(content)
    
    # Combine all analyses into one large string for the writeup
    combined_analysis = "\n\n".join(all_analyses)
    
    # Send the combined analysis to GPT-4 for summarization
    print("Sending combined analysis to GPT-4 for writeup generation...")
    final_writeup = send_to_gpt4_for_writeup(combined_analysis)
    
    if final_writeup:
        # Save the final writeup to a file
        with open(FINAL_WRITEUP_FILE, 'w', encoding='utf-8') as writeup_file:
            writeup_file.write(final_writeup)
        print(f"Final writeup saved to {FINAL_WRITEUP_FILE}.")
    else:
        print("Failed to generate final writeup.")



def main(subfolder=""):
    """
    Main function that scans a specific subfolder or the entire repo if no subfolder is provided.
    Example of subfolder: '/vllm/attention' 
    """
    # Get the list of all files in the specified subfolder
    print(f"Fetching files from the repository's subfolder: {subfolder}...")
    files = get_files_in_repo(GITHUB_API_URL, subfolder)
    
    print(f"Found {len(files)} files in {subfolder}.")
    expected_analysis_files = []  # Track expected analysis file paths
    
    for file_data in files:
        file_url = file_data['download_url']
        print(f"Analyzing file: {file_url}")
        analysis = send_file_to_gpt4(file_url, USER_PROMPT_PREFIX)
        if analysis:
            save_analysis(file_data, analysis)
            expected_analysis_files.append(file_data['path'] + ".analysis.txt")  # Add expected analysis file
            print(f"Analysis for {file_url} saved.\n")
    
    # Start a separate process to monitor and generate the final writeup
    writeup_process = Process(target=monitor_and_generate_writeup, args=(expected_analysis_files,))
    writeup_process.start()
    writeup_process.join()

if __name__ == "__main__":
    subfolder_to_scan =  "/vllm/attention/backends"
    main(subfolder=subfolder_to_scan)

if __name__ == "__main__":
    # You can specify the subfolder you want to scan by providing it as an argument
    # Example subfolder: '/vllm/attention/backends'
    subfolder_to_scan =  "/vllm/attention/backends"
    main(subfolder=subfolder_to_scan)
