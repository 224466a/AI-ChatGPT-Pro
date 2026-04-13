from transformers import pipeline

chatbot = pipeline(
    "text-generation",
    model="gpt2"
)

def generate_response(prompt, history):

    # Keep only last 3 messages (to avoid confusion)
    history = history[-3:]

    conversation = ""

    for role, msg in history:
        if role == "User":
            conversation += f"User: {msg}\n"
        else:
            conversation += f"Assistant: {msg}\n"

    conversation += f"User: {prompt}\nAssistant:"

    response = chatbot(
        conversation,
        max_length=150,
        num_return_sequences=1,
        pad_token_id=50256,
        do_sample=True,
        temperature=0.7
    )

    text = response[0]["generated_text"]

    # Extract only assistant reply
    return text.split("Assistant:")[-1].strip()