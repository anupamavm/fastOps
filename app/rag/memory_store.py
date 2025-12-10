from .embedder import embed
from .vector_store import add_document

memory = {}

def save(session_id: str, text: str):
    emb = embed(text)
    if session_id not in memory:
        memory[session_id] = []
    memory[session_id].append(text)
    add_document(text, emb)

def get(session_id: str):
    return memory.get(session_id, [])
