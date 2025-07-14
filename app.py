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
st.title("🌟 Mini Bot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None

# Initial welcome
if len(st.session_state.messages) == 0:
    render_chat_bubble("ai", "🌸 Hi! I'm Mini Bot. You can talk or type. I'm listening!")

# Record voice on button click
user_input = None
if st.button("🎤 Speak"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            st.success("Processing your voice...")
            user_input = r.recognize_google(audio)
            st.success(f"You said: {user_input}")
        except sr.WaitTimeoutError:
            st.error("⏱️ Timeout! Try again.")
        except sr.UnknownValueError:
            st.error("🤐 Couldn’t understand your voice.")
        except sr.RequestError as e:
            st.error(f"⚠️ Error with speech service: {e}")

# Optional: typed fallback
typed_input = st.chat_input("Or type your message here...")
if typed_input:
    user_input = typed_input

# Handle new user input
if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.spinner("Mini Bot is thinking..."):
        full_history = st.session_state.messages.copy()
        reply = get_gemini_response(full_history)
        st.session_state.messages.append(("model", reply))

        # Prepare voice playback for the next run
        try:
            tts = gTTS(reply)
            temp_path = os.path.join(tempfile.gettempdir(), "mini_bot_reply.mp3")
            tts.save(temp_path)
            st.session_state.pending_audio = temp_path
        except Exception as e:
            st.error(f"🎧 Voice generation error: {e}")

    # Rerun to show written message first
    st.rerun()

# Render chat messages
for role, msg in st.session_state.messages:
    render_chat_bubble(role, msg)

# After rendering, play audio if it exists
if st.session_state.pending_audio:
    try:
        audio = AudioSegment.from_file(st.session_state.pending_audio, format="mp3")
        play(audio)
        os.remove(st.session_state.pending_audio)
    except Exception as e:
        st.error(f"🎧 Voice playback error: {e}")
    st.session_state.pending_audio = None
