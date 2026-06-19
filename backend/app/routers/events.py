from typing import List 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_event import TicketEvent
from app.schemas.ticket_event import TicketEventResponse
from app.core.security import get_current_user 


router = APIRouter(
    prefix="/tickets",
    tags=["Events"]
)

@router.get(
    "/tickets/{ticket_id}/events",
    response_model=List[TicketEventResponse]
) 
def get_ticket_events(
    ticket_id: int,
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

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

    events = (
        db.query(TicketEvent)
        .options(joinedload(TicketEvent.user))
        .filter(TicketEvent.ticket_id == ticket_id)
        .order_by(TicketEvent.created_at.asc())
        .all()
    )

    db.close()