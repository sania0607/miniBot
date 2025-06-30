import google.generativeai as genai
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb import Client
import uuid  

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)  

model = genai.GenerativeModel("gemini-2.5-flash")

chroma_client = Client(Settings(allow_reset=True, anonymized_telemetry=False))
memory_store = chroma_client.create_collection("mini_bot_memory")

def summarize_chunk(chunk: list[tuple[str, str]]) -> str:
    formatted = "\n".join([f"{role}: {msg}" for role, msg in chunk])
    summary_prompt = f"Summarize this conversation:\n\n{formatted}"
    try:
        summary = model.generate_content(summary_prompt)
        return summary.text
    except Exception as e:
        return f"❌ Error while summarizing: {e}"

def embed_and_store_summary(summary: str, uid: str):
    try:
        embedding = genai.embed_content(
            model="models/embedding-001",
            content=summary,
            task_type="semantic_similarity"
        )["embedding"]
        memory_store.add(documents=[summary], embeddings=[embedding], ids=[uid])
    except Exception as e:
        print(f"❌ Error embedding/storing: {e}")

def search_relevant_memory(query: str, top_k=3) -> list[str]:
    try:
        query_embedding = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="semantic_similarity"
        )["embedding"]
        results = memory_store.query(query_embeddings=[query_embedding], n_results=top_k)
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        print(f"❌ Error during memory retrieval: {e}")
        return []

def get_gemini_response(messages: list[tuple[str, str]]) -> str:
    try:
        recent_messages = messages[-3:] 
        last_user_msg = [m[1] for m in reversed(messages) if m[0] == "user"]
        query = last_user_msg[0] if last_user_msg else ""

        relevant_memories = search_relevant_memory(query)
        memory_context = "\n\n".join(relevant_memories)

        formatted_messages = []
        for i, (role, content) in enumerate(recent_messages):
            if i == len(recent_messages) - 1 and role == "user" and memory_context:
                content = memory_context + "\n\n" + content
            formatted_messages.append({"role": role, "parts": [content]})

        response = model.generate_content(formatted_messages)
        answer = response.text

        full_chunk = recent_messages + [("model", answer)]
        summary = summarize_chunk(full_chunk)
        uid = str(uuid.uuid4())  
        embed_and_store_summary(summary, uid)

        return answer
    except Exception as e:
        return f"❌ Error: {e}"
