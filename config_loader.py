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
