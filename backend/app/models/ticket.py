from datetime import datetime 
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base 
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    description = Column(Text, nullable=False)

    status = Column(String(50), nullable=False, default="OPEN")

    priority = Column(String(50), nullable=False, default="MEDIUM")

    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    closed_at = Column(DateTime, nullable=True)

    comments = relationship(
        "TicketComment",
        back_populates="ticket"
    )

