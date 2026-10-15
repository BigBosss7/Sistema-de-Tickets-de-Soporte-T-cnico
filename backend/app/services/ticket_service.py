from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session

from app.exceptions.ticket_exceptions import (
    TicketNotFoundException,
    TechnicianNotFoundException,
    UnauthorizedTicketAccessException
)
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
       raise TechnicianNotFoundException()


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

    if current_user.role == "TECHNICIAN":
        if ticket.assigned_to_id != current_user.id:
            raise UnauthorizedTicketAccessException()

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

def get_tickets_service(
    db: Session,
    current_user: User
):

    if current_user.role == "SUPERVISOR":
        return db.query(Ticket).all()

    if current_user.role == "TECHNICIAN":
        return (
            db.query(Ticket)
            .filter(Ticket.assigned_to_id == current_user.id)
            .all()
        )

    return (
        db.query(Ticket)
        .filter(Ticket.created_by_id == current_user.id)
        .all()
    )

def get_ticket_service(
    db: Session,
    ticket_id: int,
    current_user: User
):

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if ticket is None:
        raise TicketNotFoundException()

    if current_user.role == "USER" and ticket.created_by_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your tickets"
        )

    if current_user.role == "TECHNICIAN" and ticket.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your assigned tickets"
        )

    return ticket

def test_technician_cannot_view_unassigned_ticket(db_session, auth_user):
    # Recuperamos el usuario ORM creado por la fixture
    technician = (
        db_session.query(User)
        .filter(User.email == auth_user["user"]["email"])
        .first()
    )

    # Para este test lo convertimos en técnico 
    technician.role = "TECHNICIAN"
    db_session.commit()
    db_session.refresh(technician)

    # Creamos un ticket que No está asignado al técnico
    ticket = Ticket(
        title= "Ticket privado",
        description= "Test de autorización",
        priority="MEDIUM",
        status="OPEN",
        created_by_id=technician.id,
        assigned_to_id=None,

    )

    db_session.add(ticket)
    db_session.commit()
    db_session.refresh(ticket)

    with pytest.raises(HTTPException) as exc_info:
        get_ticket_service(
            db=db_session,
            ticket_id=ticket.id,
            current_user=technician,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You con only view assigned tickets"