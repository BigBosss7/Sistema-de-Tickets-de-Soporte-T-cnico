from app.models.ticket_event import TicketEvent

def create_ticket_event(
    db,
    ticket_id,
    user_id,
    event_type,
    description
):

    event = TicketEvent(
        ticket_id=ticket_id,
        user_id=user_id,
        event_type=event_type,
        description=description
    )

    db.add(event)
    db.commit()

    return event