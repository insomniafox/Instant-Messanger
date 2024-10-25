from datetime import datetime

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    text: str
    sender_id: int
    sender_username: str
    receiver_id: int
    receiver_username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y.%m.%d %H:%M')
        }

    class Meta:
        from_attributes = True
