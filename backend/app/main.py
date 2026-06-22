from fastapi import FastAPI, HTTPException, Depends 
from typing import List, Literal  
from app.core.events import create_ticket_event
from app.core.security import (
    hash_password, 
    verify_password,
    create_access_token,
    get_current_user
)

from app.database import (
    engine,
    Base,
    SessionLocal
)
from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment
from app.models.ticket_event import TicketEvent 
from app.schemas.auth import LoginRequest 
from app.schemas.user import UserCreate, UserResponse
from app.schemas.ticket import (
    TicketCreate, 
    TicketResponse, 
    TicketAssign, 
    TicketStatusUpdate
)
from app.schemas.ticket_comment import( 
    TicketCommentCreate, 
    TicketCommentResponse,
    TicketCommentWithUserResponse
)
from app.schemas.ticket_event import TicketEventResponse
from app.routers.auth import router as auth_router
from app.routers.comments import router as comments_router
from app.routers.tickets import router as ticket_router
from app.routers.events import router as events_router
from app.routers.dashboard import router as dashboard_router
from app.routers.users import router as users_router
from sqlalchemy import func 
from sqlalchemy.orm import joinedload 
from datetime import datetime, timedelta

TicketStatus = Literal[
    "OPEN",
    "ASSIGNED",
    "IN_PROGRESS",
    "RESOLVED",
    "CLOSED"
]

app = FastAPI(
    title="Support Ticket System",
    description="API para gestionar tickets de soporte técnico.",
    version="0.1.0"
)

app.include_router(auth_router)

app.include_router(ticket_router)

app.include_router(comments_router)

app.include_router(events_router)

app.include_router(dashboard_router)

app.include_router(users_router)

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










@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):

    db = SessionLocal()

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    db.close()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )
        

    return ticket 






