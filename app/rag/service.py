import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from .embedder import embed
from .pgvector_store import search
from .db_memory_store import save, get

# Load .env from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
client = Groq(api_key=api_key)

def answer(question: str, session_id: str, chat_id: str = "default"):
    q_embed = embed(question)
    # vector search for specific chat_id
    context_docs = search(q_embed, session_id=session_id, chat_id=chat_id, top_k=3)
    memory = "\n".join(get(session_id, chat_id, limit=10))

    prompt = f"""
    Context from previous conversations:
    {context_docs}

    Recent conversation history:
    {memory}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    answer_text = response.choices[0].message.content
    save(session_id, chat_id, "user", question)
    save(session_id, chat_id, "assistant", answer_text)

    return answer_text
