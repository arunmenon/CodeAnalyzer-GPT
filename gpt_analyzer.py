import requests
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

def send_file_to_gpt4(file_content, user_prompt_prefix):
    """
    Send file content to GPT-4 for analysis.
    """
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

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

    if response.status_code != 200:
        print(f"Error analyzing content: {response.status_code}")
        return None

    result = response.json()
    return result['choices'][0]['message']['content']

def send_to_gpt4_for_writeup(content):
    """
    Send analysis content to GPT-4 for summarization.
    """
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

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

    if response.status_code != 200:
        print(f"Error analyzing content: {response.status_code}")
        return None

    result = response.json()
    return result['choices'][0]['message']['content']
