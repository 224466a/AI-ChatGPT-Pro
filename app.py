import streamlit as st
from chatbot.model import generate_response
from chatbot.auth import login
from chatbot.storage import save_chat, load_chat
theme = st.toggle("🌙 Dark Mode", value=True)
# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SECTION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }

    .login-container {
        max-width: 420px;
        margin: auto;
        margin-top: 100px;
        padding: 2rem;
        border-radius: 20px;
        background: #1c1f26;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .login-title {
        text-align: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🤖 AI Chat Login</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()
if "history" not in st.session_state:
    st.session_state.history = load_chat()   
    
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.button("🗑 Clear Chat"):
        st.session_state.history = []
        save_chat([])
        st.rerun()

    theme = st.toggle("🌙 Dark Mode", value=True)
# ---------------- CHATBOT SECTION ----------------
st.title("🤖 AI ChatGPT Clone")
st.divider()

if "history" not in st.session_state:
    st.session_state.history = load_chat()

for role, message in st.session_state.history:
    with st.chat_message("user" if role == "User" else "assistant"):
        st.write(message)

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.history.append(("User", user_input))

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            response = generate_response(user_input, st.session_state.history)

        st.write(response)

    st.session_state.history.append(("AI", response))
    save_chat(st.session_state.history)
    
    
st.title("🤖 AI ChatGPT Clone")
st.divider()
        
if st.button("🗑 Clear Chat"):
    st.session_state.history = []
    save_chat([])
    st.rerun()