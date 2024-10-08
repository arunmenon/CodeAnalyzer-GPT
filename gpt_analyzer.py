import os
import requests
from config_loader import load_system_prompt, load_user_prompt_prefix

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

def send_file_to_gpt4(file_content):
    """
    Send file content to GPT-4 for analysis, using both system and user prompts from the config file.
    """
    system_prompt = load_system_prompt()  # Load system prompt from config
    user_prompt_prefix = load_user_prompt_prefix()  # Load user prompt from config

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt_prefix}\n\n{file_content}"}
        ]
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        print(f"Error analyzing content: {response.status_code}")
        return None

    result = response.json()
    return result['choices'][0]['message']['content']

def send_to_gpt4_for_writeup(content):
    """
    Send analysis content to GPT-4 for summarization, using the system prompt from the config file.
    """
    system_prompt = load_system_prompt()  # Load system prompt from config

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please generate a detailed writeup based on the following analyses:\n\n{content}"}
        ]
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        print(f"Error analyzing content: {response.status_code}")
        return None

    result = response.json()
    return result['choices'][0]['message']['content']
