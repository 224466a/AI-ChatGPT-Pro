history = []

def add_message(role, message):
    history.append((role, message))

def get_history():
    return history  