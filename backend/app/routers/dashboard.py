from datetime import timedelta 

from fastapi import APIRouter
from sqlalchemy import func

from app.database import SessionLocal
from app.models.ticket import Ticket 


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
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

    closed_tickets = (
        db.query(Ticket)
        .filter(Ticket.closed_at.isnot(None))
        .all()
    )

    average_resolution_hours = 0

    if closed_tickets:
        total_resolution_time = timedelta()

        for ticket in closed_tickets:
            total_resolution_time += (ticket.closed_at - ticket.created_at)

        average_resolution_time = total_resolution_time / len(closed_tickets)

        average_resolution_hours = round(
            average_resolution_time.total_seconds() / 3600,
            2
        )

    db.close()

   

    return {
       "total_tickets": total_tickets,
       "open_tickets": open_tickets,
       "tickets_by_priority": dict(tickets_by_priority),
       "tickets_by_technician": dict(tickets_by_technician),
       "average_resolution_hours": average_resolution_hours 
        }


    return events