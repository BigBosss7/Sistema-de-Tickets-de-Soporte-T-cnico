from datetime import datetime 
from pydantic import BaseModel 

class EventUserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }


class TicketEventResponse(BaseModel):
    id: int
    ticket_id: int
    event_type: str
    description: str
    created_at: datetime | None
    user: EventUserResponse

    model_config = {
        "from_attributes": True
    }