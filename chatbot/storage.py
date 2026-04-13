import json

def save_chat(history):
    with open("chat_history.json", "w") as f:
        json.dump(history, f)

def load_chat():
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except:
        return []