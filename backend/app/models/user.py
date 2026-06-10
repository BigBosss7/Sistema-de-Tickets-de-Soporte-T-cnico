from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship 

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email= Column(String(255), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    comments = relationship(
        "TicketComment",
        back_populates="user"
    )
