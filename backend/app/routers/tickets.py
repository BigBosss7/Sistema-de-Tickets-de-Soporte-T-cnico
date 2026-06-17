from typing import List 
from fastapi import APIRouter, Depends 

from app.models.user import User 
from app.database import SessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketStatus
from app.core.events import create_ticket_event
from app.core.security import get_current_user

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("", response_model=TicketResponse)
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

    
    
    create_ticket_event(
        db=db,
        ticket_id=new_ticket.id,
        user_id=ticket.created_by_id,
        event_type="TICKET_CREATED",
        description="Ticket created"
    )

    db.commit()
    db.refresh(new_ticket)
    
    db.close()

    return new_ticket 

@router.get("", response_model=List[TicketResponse])
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