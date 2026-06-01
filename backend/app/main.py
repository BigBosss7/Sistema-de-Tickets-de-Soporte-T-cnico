from fastapi import FastAPI
from typing import List 
from app.database import (
    engine,
    Base,
    SessionLocal
)
from app.models.user import User
from app.schemas.user import UserResponse

app = FastAPI(
    title="Support Ticket System",
    description="API para gestionar tickets de soporte técnico.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

@app.get(
    "/",
    summary="Health check inicial",
    description="Verifica que la API está funcionando correctamente."
)
def home():
    return {
        "status": "ok",
        "message": "Support Ticket System API is running"
    }

@app.get("/health",
    summary="Health check",
    description="Verifica que la API está funcionando correctamnete"
)
def health():
    return {
        "api": "running",
        "version": "0.1.0"
    }

@app.get("/db-check")
def db_check():
    try:
        with engine.connect():
            return {"database": "connected"}
    except Exception as error:
        return {
            "database": "error",
            "detail": str(error)
        }

@app.get("/users", response_model=List[UserResponse])
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users
