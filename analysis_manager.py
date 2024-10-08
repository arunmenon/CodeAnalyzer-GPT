import os
import requests
from gpt_analyzer import send_file_to_gpt4

OUTPUT_FOLDER = "analysis_output"

def save_analysis(file_data, analysis, repo_owner, repo_name):
    """
    Save the GPT-4 analysis to a file, maintaining the directory structure.
    """
    relative_path = file_data['path']
    file_prefix = f"{repo_owner}_{repo_name}_{relative_path.replace('/', '_')}"
    analysis_file_path = os.path.join(OUTPUT_FOLDER, file_prefix + ".analysis.txt")

    os.makedirs(os.path.dirname(analysis_file_path), exist_ok=True)

    with open(analysis_file_path, 'w', encoding='utf-8') as analysis_file:
        analysis_file.write(analysis)

def process_file(file_data):
    """
    Process individual file content, analyze it with GPT-4, and save the analysis.
    """
    file_url = file_data['download_url']
    file_content = requests.get(file_url).text
    analysis = send_file_to_gpt4(file_content)
    if analysis:
        save_analysis(file_data, analysis, "vllm-project", "vllm")
        return file_data['path'] + ".analysis.txt"
    return None
