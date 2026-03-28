from fastapi import APIRouter
from app.rag.service import answer

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/query")
def rag_query(payload: dict):
    question = payload.get("question")
    session_id = payload.get("session_id", "default")
    chat_id = payload.get("chat_id", "default")  # new

    return {
        "answer": answer(question, session_id, chat_id)
    }
    