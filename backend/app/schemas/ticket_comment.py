from datetime import datetime 
from pydantic import BaseModel 

class TicketCommentCreate(BaseModel):
    message: str


class TicketCommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    created_at: datetime

    model_config = {
        "from_atributes": True
    }