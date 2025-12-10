from fastapi import APIRouter
from app.rag.service import answer

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/query")
def rag_query(payload: dict):
    question = payload.get("question")
    session_id = payload.get("session_id", "default")

    return {
        "answer": answer(question, session_id)
    }
