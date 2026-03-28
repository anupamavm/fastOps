from fastapi import APIRouter
from app.rag.service import answer , save

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/query")
def rag_query(payload: dict):
    question = payload.get("question")
    session_id = payload.get("session_id", "default")
    chat_id = payload.get("chat_id", "default")  # new

    return {
        "answer": answer(question, session_id, chat_id)
    }


@router.post("/add_context")
def add_context(payload: dict):
    """
    Add arbitrary text as context to a specific chat thread.
    """
    session_id = payload.get("session_id", "default")
    chat_id = payload.get("chat_id", "default")
    text = payload.get("text")

    if not text:
        return {"error": "No text provided"}

    save(session_id, chat_id, role="system", content=text)

    return {"status": "success", "session_id": session_id, "chat_id": chat_id}
