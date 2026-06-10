from datetime import datetime 

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey 

from app.database import Base 

from sqlalchemy.orm import relationship 

user = relationship("User", back_populates="comments")
ticket = relationship("Ticket", back_populates="comments")



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

    user = relationship("User", back_populates="comments")
    
    ticket = relationship("Ticket", back_populates="comments")