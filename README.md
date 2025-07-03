# 🤖 Mini Bot – Built with Streamlit & Google Gemini API

Welcome to **Mini Bot**, a general-purpose conversational assistant built using Google's Gemini 2.5 model and Streamlit! This chatbot takes user input as text and returns intelligent, meaningful responses in real-time.

---

## 🧠 What This Project Does

- Accepts text input from users via a chat interface  
- Sends input to the **Gemini 2.5 API**  
- Displays the AI-generated response in a clean, chat-style layout  
- Renders messages in a role-based layout (left/right), mimicking real conversation  
- Built with a focus on UX/UI and real-world API usage

---

## 🛠️ Tech Stack

| Layer    | Tool / Library                             |
|----------|--------------------------------------------|
| Frontend | `Streamlit`                                |
| Backend  | `Python`                                   |
| AI Model | `Gemini 2.5 (via Google Generative AI SDK)`|
| Styling  | Custom HTML/CSS injected into Streamlit    |
| Database | `ChromaDB`                                 |

---

## 🚀 How to Run the Bot

### 🧩 1. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install streamlit google-generativeai chromadb
```

Or use the requirements.txt:

```bash
pip install -r requirements.txt
```

### ▶️ 2. Run the App

```bash
streamlit run app.py
```

Make sure your Gemini API key is properly set before running the app.

---

## 📂 Project Structure

Mini-Bot/  
├── app.py               # Main Streamlit app  
├── chat_ui.py           # UI layout and chat logic  
├── requirements.txt     # All required Python packages  
├── README.md            # Project documentation

---

## ✨ Features to Add (Future Scope)

- Voice input/output integration  
- Persistent chat history using ChromaDB  
- Theme toggle (dark/light mode)  
- API key protection using environment variables  
- Custom system prompts/personas  
- Better error handling and loading states

---


