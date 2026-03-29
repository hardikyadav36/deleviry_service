from fastapi import APIRouter, FastAPI
from sqlalchemy.orm import Session
from app.database.depends import get_db
from app.models.user import User
from fastapi import Depends
router = APIRouter()

@router.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user