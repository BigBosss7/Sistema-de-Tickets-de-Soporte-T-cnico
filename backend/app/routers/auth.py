from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.core.security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(credentials: LoginRequest):
    db= SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == credentials.email)
        .first()
    )

    if user is None:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid credentails"
        )

    if not verify_password(
        credentials.password,
        user.password_hash
    ):

      db.close()
      raise HTTPException(
        satus_code=401,
        detal="Invalid credentials"
      )

    db.close()

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "user_id": "bearer"
        
    }