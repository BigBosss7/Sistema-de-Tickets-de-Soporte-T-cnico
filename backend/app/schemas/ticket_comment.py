from datetime import datetime 
from pydantic import BaseModel


class CommentUserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }

class TicketCommentCreate(BaseModel):
    message: str


class TicketCommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    created_at: datetime | None

    model_config = {
        "from_atributes": True
    }

class TicketCommentWithUserResponse(BaseModel):
    id: int
    ticket_id: int
    message: str
    created_at: datetime | None 
    user: CommentUserResponse

    model_config = {
        "from_attributes": True
    }