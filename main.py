from fastapi import FastAPI
from app.routers import user_router
from app.config import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastOps API", version="1.0.0")

app.include_router(user_router)
