from typing import List 
from fastapi import APIRouter, Depends, HTTPException 
from datetime import datetime

from app.models.user import User 
from app.database import SessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import (
    TicketCreate, 
    TicketResponse, 
    TicketStatus, 
    TicketAssign,
    TicketStatusUpdate
)
from app.core.events import create_ticket_event
from app.core.security import get_current_user
from app.core.permissions import require_supervisor, require_technician_or_supervisor 
from app.services.ticket_service import (
    create_ticket_service,
    assign_ticket_service,
    update_ticket_status_service,
    get_ticket_service
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    db = SessionLocal()

    new_ticket = create_ticket_service(
        db=db,
        ticket=ticket
    )

    db.close()

    return new_ticket 

@router.get("", response_model=List[TicketResponse])
def get_tickets(
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    tickets = get_tickets_service(
        db=db,
        current_user=current_user
    )

    db.close()
    
    return tickets 

@router.patch("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: int, 
    assignment: TicketAssign,
    current_user: User = Depends(require_supervisor)
    ):

    db = SessionLocal()

    ticket = assign_ticket_service(
        db=db,
        ticket_id=ticket_id,
        assignment=assignment,
        current_user=current_user
    )

    db.close()
   
  
    return ticket 

@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int, 
    status_update: TicketStatusUpdate,
    current_user: User = Depends(require_technician_or_supervisor)
    ):
    db= SessionLocal()

    ticket =  update_ticket_status_service(
        db=db,
        ticket_id=ticket_id,
        status_update=status_update,
        current_user=current_user
    )

    db.close()

    return ticket 

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user)
    ):

    db = SessionLocal()

    ticket = get_ticket_service(
        db=db,
        ticket_id=ticket_id,
        current_user=current_user
    )

    db.close()

    return ticket 


