import requests
import os

API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def generate_response(prompt, history):

    # Combine conversation
    conversation = ""
    for role, msg in history:
        conversation += f"{role}: {msg}\n"

    conversation += f"User: {prompt}\nAI:"

    payload = {
        "inputs": conversation,
        "parameters": {
            "max_new_tokens": 100
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    result = response.json()

    return result[0]["generated_text"].split("AI:")[-1].strip()
