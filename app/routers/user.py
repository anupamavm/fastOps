from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import User, UserCreate
from app.services import create_user
from app.config import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
