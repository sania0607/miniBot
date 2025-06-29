from google import genai

#  Configure Gemini client
client = genai.Client(api_key="AIzaSyAZgBYZXHTPB9RJfIJxCzF0qCwxS9DFSYM")  # Replace with your actual key

def get_gemini_response(prompt):
    try:
        # Send the prompt to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"




