from fastapi import FastAPI
from app.routers import user_router, rag_router
from app.config import Base, engine
from app.rag import pgvector_store

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize pgvector extension
try:
    pgvector_store.init_extension()
except Exception as e:
    print(f"Warning: Could not initialize pgvector extension: {e}")

app = FastAPI(title="FastOps API", version="1.0.0")

app.include_router(user_router)
app.include_router(rag_router)