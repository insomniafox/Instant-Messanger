from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.models.users.models import User
from src.services.auth.utils import get_password_hash
from src.services.users.exceptions import UserFotFoundException


class UserService:
    @classmethod
    async def get_users(
        cls,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        **filters
    ) -> Sequence[User]:
        result = await db.execute(select(User).filter_by(**filters))
        return result.scalars().all()

    @classmethod
    async def get_user(
        cls,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        raise_exception: bool = True,
        **filters
    ) -> User | None:
        result = await db.execute(select(User).filter_by(**filters))
        user = result.scalars().first()
        if not user and raise_exception:
            raise UserFotFoundException
        return user

    @classmethod
    async def create_user(
        cls,
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> User:
        user = User(
            username=username,
            password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
