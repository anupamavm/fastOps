from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from pgvector.sqlalchemy import Vector
from app.config.database import Base
from datetime import datetime

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    )


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=False)  # 384 dimensions for all-MiniLM-L6-v2
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index('idx_embedding_vector', 'embedding', postgresql_using='ivfflat'),
    )
