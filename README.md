# LLM-Assisted GitHub Code Analyzer

### Flowchart
```plaintext
+------------------------------------------+
|            Start the Analyzer            |
+-------------------+----------------------+
                    |
                    v
  +--------------------------------------+
  | Load Configuration (repo, prompts)   |
  +--------------------------------------+
                    |
                    v
  +--------------------------------------+
  | Fetch Files from GitHub Repository   |
  +--------------------------------------+
                    |
                    v
+-----------------------------------------+
|  Analyze Files in Parallel Using GPT-4  |
+-----------------------------------------+
                    |
                    v
+-----------------------------------------+
| Save Analysis and Maintain Folder Structure |
+-----------------------------------------+
                    |
                    v
+-----------------------------------------+
| Monitor Completion of All File Analysis  |
+-----------------------------------------+
                    |
                    v
+-----------------------------------------+
|   Generate Final Writeup Using GPT-4     |
+-----------------------------------------+
                    |
                    v
+-----------------------------------------+
|               End Process               |
+-----------------------------------------+
```

### Overview
This project is an LLM-assisted code analyzer that leverages GPT-4 to recursively scan a specified GitHub repository, analyze its contents, and generate detailed writeups. The application retrieves the files from the repository, processes them in parallel using GPT-4, and saves the analyses. After all analyses are completed, it compiles the results into a final writeup.

### Project Structure

```plaintext
.
├── analysis_manager.py   # Handles file processing and saving analyzed data
├── config_loader.py      # Loads the configuration for prompts and GitHub details
├── gpt_analyzer.py       # Interacts with GPT-4 API to analyze files and generate summaries
├── github_helper.py      # Fetches files from the GitHub repository
├── writeup_manager.py    # Monitors analysis completion and generates final writeups
├── main.py               # Main entry point for the application
├── config.txt            # Configuration file for system prompts, GitHub repo details, etc.
└── README.md             # This file
```

### Module Walkthrough

1. **`main.py`**  
   This is the main orchestrator of the application. It fetches repository details from the config file, initiates file retrieval, sends them for GPT-4 analysis, and triggers the final writeup generation.
   
2. **`config_loader.py`**  
   Handles loading the repository details, system prompts, and user prompts from the configuration file.

3. **`gpt_analyzer.py`**  
   This module interfaces with GPT-4 to analyze code files and generate a detailed final writeup. It uses prompts loaded from the config file.

4. **`github_helper.py`**  
   Responsible for interacting with GitHub's API to recursively fetch files from the specified repository.

5. **`analysis_manager.py`**  
   Manages the processing of files by fetching their contents, sending them to GPT-4 for analysis, and saving the results.

6. **`writeup_manager.py`**  
   Monitors the progress of the analyses and generates a detailed writeup once all files are analyzed.

### Configuration

The analyzer is easily configured via the `config.txt` file:

```plaintext
SYSTEM_PROMPT=You are a helpful assistant.
USER_PROMPT_PREFIX=Please analyze the following code and give intuitive explanation:
REPO_OWNER=vllm-project
REPO_NAME=vllm
SUBFOLDER_TO_SCAN=/vllm/attention
```

- **SYSTEM_PROMPT**: Defines the assistant's role in providing helpful information during file analysis.
- **USER_PROMPT_PREFIX**: Customizes the way files are analyzed by GPT-4.
- **REPO_OWNER, REPO_NAME, SUBFOLDER_TO_SCAN**: Specify the repository and subfolder to be scanned and analyzed.

### Running the Analyzer

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/repo-analyzer.git
   cd repo-analyzer
   ```

2. **Set Environment Variables** for GitHub and OpenAI API keys:
   ```bash
   export GITHUB_ACCESS_TOKEN=your_github_access_token
   export OPENAI_API_KEY=your_openai_api_key
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Analyzer**:
   Simply run the main script:
   ```bash
   python main.py
   ```

The analyzer will recursively scan the configured GitHub repository and generate a final writeup based on the GPT-4 analysis of each file.