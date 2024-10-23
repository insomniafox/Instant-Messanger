from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.models.users.models import User
from src.services.users.exceptions import UserAlreadyExistsException
from src.services.users.service import UserService


async def register_user(
    username: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> User:
    user = await UserService.get_user(username=username, db=db, raise_exception=False)
    if user:
        raise UserAlreadyExistsException
    user = await UserService.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        db=db
    )
    return user
