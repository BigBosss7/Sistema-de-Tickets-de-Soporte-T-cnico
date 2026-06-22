from typing import List 

from fastapi import APIRouter, Depends

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse 
from app.core.security import get_current_user, hash_password 


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("", response_model=List[UserResponse])
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()


    return users

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }