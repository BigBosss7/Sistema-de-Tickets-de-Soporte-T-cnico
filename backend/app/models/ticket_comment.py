from datetime import datetime 

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey 

from app.database import Base 


class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    message = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)