from fastapi import FastAPI, HTTPException
from typing import List 
from app.database import (
    engine,
    Base,
    SessionLocal
)
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.user import UserCreate, UserResponse
from app.schemas.ticket import TicketCreate, TicketResponse, TicketAssign

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

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user

@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    db = SessionLocal()

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        created_by_id=ticket.created_by_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    db.close()

    return new_ticket 

@app.get("/tickets", response_model=List[TicketResponse])
def get_tickets():

    db = SessionLocal()

    tickets = db.query(Ticket).all() # SELECT * FROM tickets 

    db.close()

    return tickets

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

@app.patch("/tickets/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(ticket_id: int, assignment: TicketAssign):
    db = SessionLocal()

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

   
    technician = (
        db.query(User)
        .filter(User.id == assignment.assigned_to_id)
        .first()
    )

    if technician is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Technician not found"
        )

    if technician.role != "TECHNICIAN":
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Only technicians can be assigned tickets"
        )

    ticket.assigned_to_id = assignment.assigned_to_id
    ticket.status = "ASSIGNED"

    db.commit()
    db.refresh(ticket)
    db.close()

    return ticket 