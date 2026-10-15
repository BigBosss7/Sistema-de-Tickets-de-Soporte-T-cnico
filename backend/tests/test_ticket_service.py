import pytest 

from fastapi import HTTPException

from app.models.user import User
from app.models.ticket import Ticket 
from app.services.ticket_service import get_ticket_service
from app.exceptions.ticket_exceptions import TicketNotFoundException

def test_get_ticket_service_existing(db_session, auth_user):
    # crea ticket previamente
    # Luego llamar directamente al service
    # Finalmente validar el resultado 
    pass 


def test_get_ticket_service_not_found(db_session, auth_user):
    current_user = (
        db_session.query(User)
        .filter(User.email == auth_user["user"]["email"])
        .first()
    )
    with pytest.raises(TicketNotFoundException):
        get_ticket_service(
            db=db_session,
            ticket_id=999999,
            current_user=current_user    
        )

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
    assert exc_info.value.detail == "You can only view your assigned tickets"