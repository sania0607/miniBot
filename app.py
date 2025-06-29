import streamlit as st
from utils import get_gemini_response 

# Page setup
st.set_page_config(
    page_title="Mini Bot ",
    layout="centered"
)

# CSS Styling
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .chat-bubble {
            padding: 1rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            max-width: 75%;
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.5;
        }
        .user {
            align-self: flex-end;
            background-color: #00755e; /* Deep mint green */
            color: white;
            text-align: right;
        }
        .ai {
            align-self: flex-start;
            background-color: #e6e6e6; /* Soft grey */
            color: #000000;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🌟 Mini Bot")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show welcome message if empty
if len(st.session_state.messages) == 0:
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-bubble ai">
            <strong>Mini Bot:</strong><br>
            🌸 Hi there! I'm <b>Mini Bot</b> — your AI bestie!<br>
            Ask me anything: coding help, project ideas, or even what's for lunch — I'm here for it ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

# Handle user message
if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.spinner("Mini Bot is typing..."):
        reply = get_gemini_response(user_input)
        st.session_state.messages.append(("ai", reply))

# Display chat history
for role, msg in st.session_state.messages:
    bubble_class = "user" if role == "user" else "ai"
    label = "You" if role == "user" else "Mini Bot"
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-bubble {bubble_class}">
            <strong>{label}:</strong><br>{msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

