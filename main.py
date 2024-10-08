from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process
from github_helper import get_files_in_repo
from analysis_manager import process_file
from writeup_manager import monitor_and_generate_writeup
from tqdm import tqdm  # Progress bar
from config_loader import load_repo_details


# Base GitHub API URL for repository content

def main(subfolder=""):
    """
    Main function that scans a specific subfolder or the entire repo if no subfolder is provided.
    """
    # Load repository details from the config file
    repo_owner, repo_name, subfolder = load_repo_details()

    GITHUB_API_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"


    print(f"Fetching files from the repository's subfolder: {subfolder}...")

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
            futures = [executor.submit(process_file, file_data) for file_data in files]
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
    main()
