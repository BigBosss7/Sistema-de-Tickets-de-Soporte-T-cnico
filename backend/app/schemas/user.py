from datetime import datetime
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime | None

    model_config = {
        "from_atributes": True
    }