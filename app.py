import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os

from services.gemini_service import get_gemini_response
from components.chat_ui import render_chat_bubble, inject_css

# Page configuration
st.set_page_config(page_title="Mini Bot", layout="centered")
inject_css()
st.title("🌟 Mini Bot - Voice Assistant")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.audio_files = {}

if "pending_bot" not in st.session_state:
    st.session_state.pending_bot = False

# Initial bot greeting
if not st.session_state.messages:
    render_chat_bubble("ai", "🌸 Hi! I'm Mini Bot. You can talk or type. I'm listening!")

# Display chat history
st.markdown('<div class="chat-area">', unsafe_allow_html=True)
for i, (role, msg) in enumerate(st.session_state.messages):
    audio_file = st.session_state.audio_files.get(i)
    render_chat_bubble(role, msg, audio_file)
st.markdown('</div>', unsafe_allow_html=True)

# Bot response handling
if st.session_state.pending_bot:
    last_user_msg = st.session_state.messages[-1][1]
    with st.spinner("Mini Bot is thinking..."):
        try:
            # Call Gemini API
            reply = get_gemini_response(st.session_state.messages)
            st.session_state.messages.append(("ai", reply))

            # Convert response to audio
            tts = gTTS(reply)
            audio_path = os.path.join(tempfile.gettempdir(), f"mini_bot_reply_{len(st.session_state.messages)}.mp3")
            tts.save(audio_path)
            st.session_state.audio_files[len(st.session_state.messages) - 1] = audio_path

        except Exception as e:
            st.session_state.messages.append(("ai", f"❌ Error: {e}"))

        finally:
            st.session_state.pending_bot = False
            st.rerun()

# Input Section: Text and Voice
st.markdown('<div class="fixed-input-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])

# Voice Input Button
with col1:
    if st.button("🎤 Hold to Speak"):
        with st.spinner("Listening..."):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                    user_voice = recognizer.recognize_google(audio)
                    st.session_state.messages.append(("user", user_voice))
                    st.session_state.pending_bot = True
                    st.rerun()
                except sr.WaitTimeoutError:
                    st.error("⏱️ Timeout! Please try again.")
                except sr.UnknownValueError:
                    st.error("🤔 Sorry, I didn't catch that. Try again.")
                except sr.RequestError as e:
                    st.error(f"⚠️ Speech recognition error: {e}")
                except Exception as e:
                    st.error(f"🎙️ Unexpected voice error: {e}")

# Text Input
with col2:
    user_text = st.chat_input("Or type your message here...")
    if user_text:
        st.session_state.messages.append(("user", user_text))
        st.session_state.pending_bot = True
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
