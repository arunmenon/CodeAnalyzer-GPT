from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process
from config_loader import load_user_prompt_prefix
from github_helper import get_files_in_repo
from analysis_manager import process_file
from writeup_manager import monitor_and_generate_writeup
from tqdm import tqdm  # Progress bar

REPO_OWNER = 'vllm-project'
REPO_NAME = 'vllm'

# Base GitHub API URL for repository content
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents"

def main(subfolder=""):
    """
    Main function that scans a specific subfolder or the entire repo if no subfolder is provided.
    """
    print(f"Fetching files from the repository's subfolder: {subfolder}...")
    USER_PROMPT_PREFIX = load_user_prompt_prefix()

    # Fetch files
    files = get_files_in_repo(GITHUB_API_URL, subfolder)
    if not files:
        print(f"No files found in {subfolder}. Exiting.")
        return

    print(f"Found {len(files)} files in {subfolder}.")
    expected_analysis_files = []
    folder_hierarchy = {}

    # Using tqdm progress bar
    with tqdm(total=len(files), desc="Analyzing files", ncols=100, unit="file") as pbar:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_file, file_data, USER_PROMPT_PREFIX) for file_data in files]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    expected_analysis_files.append(result)
                    folder_hierarchy[result] = f"vllm-project/vllm/{subfolder}"
                pbar.update(1)  # Update progress bar

    print("All files submitted for analysis. Monitoring for completion...")

    # Start writeup process
    writeup_process = Process(target=monitor_and_generate_writeup, args=(expected_analysis_files, folder_hierarchy))
    writeup_process.start()
    writeup_process.join()

    print("Writeup process completed successfully.")

if __name__ == "__main__":
    main(subfolder="/vllm/attention")
