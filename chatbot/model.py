import requests
import os
import time

API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def generate_response(prompt, history):

    conversation = ""
    for role, msg in history:
        conversation += f"{role}: {msg}\n"

    conversation += f"User: {prompt}\nAI:"

    payload = {
        "inputs": conversation,
        "parameters": {"max_new_tokens": 100}
    }

    for _ in range(3):  # 🔁 retry 3 times
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"].split("AI:")[-1].strip()

        time.sleep(3)  # wait before retry

    return "⚠️ AI is busy. Please try again."
