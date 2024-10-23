from datetime import datetime

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    text: str
    sender_id: int
    receiver_id: int
    created_at: datetime
    updated_at: datetime
