import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import tempfile
import os

from services.gemini_service import get_gemini_response
from components.chat_ui import render_chat_bubble, inject_css



st.set_page_config(page_title="Mini Bot", layout="centered")
inject_css()
st.title("🌟 Mini Bot - Voice Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.audio_files = {}  # To store audio for each message

# Initial welcome
if len(st.session_state.messages) == 0:
    render_chat_bubble("ai", "🌸 Hi! I'm Mini Bot. You can talk or type. I'm listening!")

# Voice input section
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🎤 Hold to Speak", key="voice_button"):
        with st.spinner("Listening..."):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=7)
                    user_input = r.recognize_google(audio)
                    st.session_state.messages.append(("user", user_input))
                    st.rerun()
                except sr.WaitTimeoutError:
                    st.error("⏱️ Timeout! Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Text input
with col2:
    user_input = st.chat_input("Or type your message here...")

# Handle text input
if user_input:
    st.session_state.messages.append(("user", user_input))

# Process the latest message
if st.session_state.messages and st.session_state.messages[-1][0] == "user":
    last_user_msg = st.session_state.messages[-1][1]
    
    with st.spinner("Mini Bot is thinking..."):
        full_history = st.session_state.messages.copy()
        reply = get_gemini_response(full_history)
        st.session_state.messages.append(("model", reply))

        # Generate and save audio
        try:
            tts = gTTS(reply)
            temp_path = os.path.join(tempfile.gettempdir(), f"mini_bot_reply_{len(st.session_state.messages)}.mp3")
            tts.save(temp_path)
            st.session_state.audio_files[len(st.session_state.messages)-1] = temp_path
        except Exception as e:
            st.error(f"🎧 Voice generation error: {e}")

# Display all messages
for i, (role, msg) in enumerate(st.session_state.messages):
    audio_path = st.session_state.audio_files.get(i)
    render_chat_bubble(role, msg, audio_path)

# Auto-play the latest audio
if st.session_state.messages and st.session_state.messages[-1][0] == "model":
    latest_audio = st.session_state.audio_files.get(len(st.session_state.messages)-1)
    if latest_audio:
        try:
            audio = AudioSegment.from_file(latest_audio, format="mp3")
            play(audio)
        except Exception as e:
            st.error(f"🎧 Voice playback error: {e}")
