import os
import time
from gpt_analyzer import send_to_gpt4_for_writeup

OUTPUT_FOLDER = "analysis_output"
FINAL_WRITEUP_FILE = "final_writeup.txt"

def monitor_and_generate_writeup(expected_analysis_files, folder_hierarchy):
    """
    Monitors the analysis folder and triggers writeup generation once all analysis files are complete.
    """
    print(f"Expecting {len(expected_analysis_files)} analysis files...")

    while True:
        completed_analysis_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(OUTPUT_FOLDER)
            for file in files if file.endswith(".analysis.txt")
        ]

        if len(completed_analysis_files) >= len(expected_analysis_files):
            print(f"All {len(completed_analysis_files)} analysis files are completed. Generating writeup...")
            generate_writeup_from_analysis(completed_analysis_files, folder_hierarchy)
            break
        else:
            print(f"Only {len(completed_analysis_files)} of {len(expected_analysis_files)} files completed. Waiting...")
            time.sleep(10)

def generate_writeup_from_analysis(completed_analysis_files, folder_hierarchy):
    """
    Generates the final writeup based on the completed analysis files.
    """
    all_analyses = []
    for analysis_file_path in completed_analysis_files:
        with open(analysis_file_path, 'r', encoding='utf-8') as analysis_file:
            content = analysis_file.read()
            folder_info = folder_hierarchy.get(analysis_file_path, "")
            all_analyses.append(f"Folder: {folder_info}\n{content}")

    combined_analysis = "\n\n".join(all_analyses)
    final_writeup = send_to_gpt4_for_writeup(combined_analysis)

    folder_prefix = folder_hierarchy.get(completed_analysis_files[0], "analysis").replace("/", "_")
    final_writeup_file = os.path.join(OUTPUT_FOLDER, f"{folder_prefix}_writeup.txt")

    if final_writeup:
        with open(final_writeup_file, 'w', encoding='utf-8') as writeup_file:
            writeup_file.write(final_writeup)
        print(f"Final writeup saved to {final_writeup_file}.")
    else:
        print("Failed to generate final writeup.")
