import streamlit as st

def render_chat_bubble(role: str, msg: str):
    bubble_class = "user" if role == "user" else "ai"
    label = "You" if role == "user" else "Mini Bot"
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-bubble {bubble_class}">
            <strong>{label}:</strong><br>{msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

def inject_css():
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
