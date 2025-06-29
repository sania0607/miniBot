import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)  # <- This sets the API key

model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(messages: list[tuple[str, str]]) -> str:
    try:
        formatted_messages = [{"role": role, "parts": [content]} for role, content in messages]
        response = model.generate_content(formatted_messages)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"
