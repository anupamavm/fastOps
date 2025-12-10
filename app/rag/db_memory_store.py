from sqlalchemy.orm import Session
from app.models.chat import ChatHistory
from app.config.database import SessionLocal
from .embedder import embed
from .pgvector_store import add_document

def save(session_id: str, role: str, content: str):
    """Save a chat message to the database"""
    db = SessionLocal()
    try:
        # Save to chat history
        chat_msg = ChatHistory(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(chat_msg)
        db.commit()
        
        # Also add to vector store for semantic search
        emb = embed(content)
        add_document(session_id, content, emb)
    finally:
        db.close()

def get(session_id: str, limit: int = 10):
    """Get recent chat history for a session"""
    db = SessionLocal()
    try:
        messages = db.query(ChatHistory)\
            .filter(ChatHistory.session_id == session_id)\
            .order_by(ChatHistory.timestamp.desc())\
            .limit(limit)\
            .all()
        
        # Return in chronological order
        return [f"{msg.role}: {msg.content}" for msg in reversed(messages)]
    finally:
        db.close()

def clear(session_id: str):
    """Clear chat history for a session"""
    db = SessionLocal()
    try:
        db.query(ChatHistory)\
            .filter(ChatHistory.session_id == session_id)\
            .delete()
        db.commit()
    finally:
        db.close()
