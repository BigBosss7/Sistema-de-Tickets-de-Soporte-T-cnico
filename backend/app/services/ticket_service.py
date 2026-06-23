from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User

from app.schemas.ticket import (
    TicketCreate, 
    TicketAssign,
    TicketStatusUpdate
)


from app.core.events import create_ticket_event 


def create_ticket_service(
    db: Session,
    ticket: TicketCreate
):

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

   return new_ticket

def assign_ticket_service(
    db: Session,
    ticket_id: int,
    assignment: TicketAssign,
    current_user: User
):

   ticket = (
       db.query(Ticket)
       .filter(Ticket.id == ticket_id)
       .first()    
   )

   if ticket is None:
      raise HTTPException(
        status_code=404,
        detail="Ticket not found"
      )

   technician = (
    db.query(User)
    .filter(User.id == assignment.assigned_to_id)
    .first()
   ) 

   if technician is None:
       raise HTTPException(
            status_code=404,
            deatail="Technician not found"
       )  

   if technician.role != "TECHNICIAN":
       raise HTTPException(
        status_code=400,
        detail="Only technicians can be assigned tickets"
       )

   ticket.assigned_to_id = assignment.assigned_to_id
   ticket.status = "ASSIGNED"

   create_ticket_event(
    db=db,
    ticket_id=ticket.id,
    user_id=current_user.id,
    event_type="TICKET_ASSIGNED",
    description=f"Ticket assigned to user {assignment.assigned_to_id}"
   )

   db.commit()
   db.refresh(ticket)

   return ticket 


def update_ticket_status_service(
    db: Session,
    ticket_id: int,
    status_update: TicketStatusUpdate,
    current_user: User
):

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.status = status_update.status

    if status_update.status == "CLOSED":
        ticket.closed_at = datetime.utcnow()
    else:
        ticket.closed_at = None

    create_ticket_event(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        event_type="STATUD_CHANGED",
        description=f"Status changed to {status_update.status}"
    )

    db.commit()
    db.refresh(ticket)

    return ticket 