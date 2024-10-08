import os

def load_user_prompt_prefix(config_file='config.txt'):
    """Loads the user prompt prefix from a config file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found.")
    
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('USER_PROMPT_PREFIX'):
                return line.split('=', 1)[1].strip()  # Strip any extra spaces or newlines
    
    raise ValueError("USER_PROMPT_PREFIX not found in the config file.")

def load_system_prompt(config_file='config.txt'):
    """Loads the system prompt from a config file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found.")
    
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('SYSTEM_PROMPT'):
                return line.split('=', 1)[1].strip()  # Strip any extra spaces or newlines
    
    raise ValueError("SYSTEM_PROMPT not found in the config file.")

def load_repo_details(config_file='config.txt'):
    """Loads the repository details (owner, name, subfolder) from a config file."""
    repo_owner = repo_name = subfolder = None
    
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found.")
    
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('REPO_OWNER'):
                repo_owner = line.split('=', 1)[1].strip()
            elif line.startswith('REPO_NAME'):
                repo_name = line.split('=', 1)[1].strip()
            elif line.startswith('SUBFOLDER_TO_SCAN'):
                subfolder = line.split('=', 1)[1].strip()

    if not repo_owner or not repo_name or not subfolder:
        raise ValueError("REPO_OWNER, REPO_NAME, or SUBFOLDER_TO_SCAN missing from the config file.")
    
    return repo_owner, repo_name, subfolder