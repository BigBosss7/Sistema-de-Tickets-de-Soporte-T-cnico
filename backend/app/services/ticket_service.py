from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
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