from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import User, UserCreate
from app.services import create_user, get_user , get_all_users
from app.config import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=User)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@router.get("/", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)
