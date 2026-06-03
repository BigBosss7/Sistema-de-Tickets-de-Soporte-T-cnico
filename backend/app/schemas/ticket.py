from datetime import datetime
from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str = "MEDIUM"
    created_by_id: int

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_by_id: int 
    assigned_to_id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    closed_at: datetime | None

    model_config = {
        "from_attributes": True
    }

class TicketAssign(BaseModel):
    assigned_to_id: int