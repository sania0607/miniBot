from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key safely
api_key = os.getenv("GEMINI_API_KEY")

# Check if key is found
if not api_key:
    raise ValueError("⚠️ API Key not found! Please set GEMINI_API_KEY in your .env file.")

# Configure Gemini client
client = genai.Client(api_key=api_key)

def get_gemini_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"




