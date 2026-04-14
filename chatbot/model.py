from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN")
)

def generate_response(prompt, history):

    messages = []

    for role, msg in history:
        if role == "User":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})

    messages.append({"role": "user", "content": prompt})

    response = client.chat_completion(
        model="HuggingFaceH4/zephyr-7b-beta",
        messages=messages,
        max_tokens=200
    )

    return response.choices[0].message["content"]
