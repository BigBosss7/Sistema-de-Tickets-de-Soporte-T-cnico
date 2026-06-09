from fastapi import FastAPI, HTTPException, Depends 
from typing import List, Literal  
from app.core.security import (
    hash_password, 
    verify_password,
    create_access_token,
    get_current_user,
    require_supervisor
) 
from app.database import (
    engine,
    Base,
    SessionLocal
)
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.auth import LoginRequest 
from app.schemas.user import UserCreate, UserResponse
from app.schemas.ticket import (
    TicketCreate, 
    TicketResponse, 
    TicketAssign, 
    TicketStatusUpdate
)
from sqlalchemy import func 


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

@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }


@app.post("/users", response_model=UserResponse)
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
def get_tickets(
    status: TicketStatus | None = None, 
    assigned_to: int | None = None,
    current_user: User = Depends(get_current_user)
    ):

    db = SessionLocal()

    query = db.query(Ticket)

    if current_user.role == "USER":
        query = query.filter(Ticket.created_by_id == current_user.id)

    if current_user.role == "TECHNICIAN":
        query = query.filter(Ticket.assigned_to_id == current_user.id)

    if status:
        query = query.filter(Ticket.status == status)

    if assigned_to and current_user.role == "SUPERVISOR":
        query = query.filter(Ticket.assigned_to_id == assigned_to)

    tickets = query.all()

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
def assign_ticket(
    ticket_id: int, 
    assignment: TicketAssign,
    current_user: User = Depends(require_supervisor)
    ):

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

@app.patch("/tickets/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int, 
    status_update: TicketStatusUpdate,
    current_user: User = Depends(get_current_user)
    ):
    db= SessionLocal()

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    
    if ticket is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

        if current_user.role == "TECHNICIAN":
            if ticket.assigned_to_id != current_user.id:

                db.close()

                raise HTTPException(
                  status_code=403,
                  detail="You can only update your assigned tickets"
                )


    ticket.status = status_update.status

    db.commit()
    db.refresh(ticket)
    db.close()

    return ticket 


@app.get("/dashboard/stats")
def dashboard_stats():
        db = SessionLocal()

        total_tickets = db.query(Ticket).count()

        open_tickets = (
            db.query(Ticket)
            .filter(Ticket.status == "OPEN")
            .count()
        )

        tickets_by_priority = (
            db.query(Ticket.priority, func.count(Ticket.id))
            .group_by(Ticket.priority)
            .all()
        )   

        tickets_by_technician = (
            db.query(Ticket.assigned_to_id, func.count(Ticket.id))
            .filter(Ticket.assigned_to_id.isnot(None))
            .group_by(Ticket.assigned_to_id)
            .all()
        )

        db.close()

        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "tickets_by_priority": dict(tickets_by_priority),
            "tickets_by_technician": dict(tickets_by_technician)
        }

@app.post("/login")
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