from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


class BaseUserSchema(BaseModel):
    username: constr(max_length=50)
    first_name: constr(max_length=64)
    last_name: constr(max_length=64)
    # telegram_id: Optional[str] = None


class UserSchema(BaseUserSchema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserRegisterSchema(BaseUserSchema):
    password: constr(max_length=128)


class UserLoginSchema(BaseModel):
    username: constr(max_length=50)
    password: constr(max_length=128)


class RefreshTokenSchema(BaseModel):
    refresh_token: str
