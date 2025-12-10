from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.chat import DocumentEmbedding
from app.config.database import SessionLocal
import numpy as np

class PgVectorStore:
    def __init__(self):
        self.embedding_dim = 384
    
    def init_extension(self):
        """Initialize pgvector extension in PostgreSQL"""
        db = SessionLocal()
        try:
            db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            db.commit()
        finally:
            db.close()
    
    def add_document(self, session_id: str, text: str, embedding):
        """Add a document with its embedding to the database"""
        db = SessionLocal()
        try:
            # Convert numpy array to list for pgvector
            embedding_list = embedding.tolist() if hasattr(embedding, 'tolist') else embedding
            
            doc_embedding = DocumentEmbedding(
                session_id=session_id,
                content=text,
                embedding=embedding_list
            )
            db.add(doc_embedding)
            db.commit()
        finally:
            db.close()
    
    def search(self, query_embedding, session_id: str = None, top_k: int = 3):
        """Search for similar documents using cosine similarity"""
        db = SessionLocal()
        try:
            # Convert numpy array to list
            embedding_list = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding
            embedding_str = "[" + ",".join(map(str, embedding_list)) + "]"
            
            # Build query with optional session filter
            query = text("""
                SELECT content, 
                       1 - (embedding <=> :embedding::vector) AS similarity
                FROM document_embeddings
                WHERE (:session_id IS NULL OR session_id = :session_id)
                ORDER BY embedding <=> :embedding::vector
                LIMIT :top_k
            """)
            
            result = db.execute(
                query,
                {
                    "embedding": embedding_str,
                    "session_id": session_id,
                    "top_k": top_k
                }
            )
            
            return [row[0] for row in result]
        finally:
            db.close()

# Singleton instance
_store = PgVectorStore()

def init_extension():
    _store.init_extension()

def add_document(session_id: str, text: str, embedding):
    _store.add_document(session_id, text, embedding)

def search(query_embedding, session_id: str = None, top_k: int = 3):
    return _store.search(query_embedding, session_id, top_k)
