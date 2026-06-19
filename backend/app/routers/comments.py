from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentResponse,
    TicketCommentWithUserResponse
)
from app.core.security import get_current_user
from app.core.events import create_ticket_event


router = APIRouter(
    prefix="/ticket",
    tags=["Comments"]
)

@router.post(
    "/{ticket_id}/comments",
    response_model=TicketCommentResponse
)
def create_ticket_comment(
    ticket_id: int,
    comment: TicketCommentCreate,
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

    new_comment = TicketComment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        message=comment.message
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    create_ticket_event(
        db=db,
        ticket_id=ticket_id,
        user_id=current_user.id,
        event_type="COMMENT_ADDED",
        description="Comment added to ticket"
    )

    db.commit()
    db.refresh(new_comment)

    db.close()

    return new_commment

@router.get(
    "/tickets/{ticket_id}/comments",
    response_model=List[TicketCommentWithUserResponse]
)
def get_ticket_comments(
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

    comments = (
        db.query(TicketComment)
        .options(joinedload(TicketComment.user))
        .filter(TicketComment.ticket_id == ticket_id)
        .order_by(TicketComment.created_at.asc())
        .all()
    )

    
    db.close()

    return comments 