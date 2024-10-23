from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.services.auth.auth import create_access_token
from src.services.users.exceptions import UserHasNoAccess
from src.services.telegram.exceptions import UserHasNoTelegramLinked
from src.services.telegram.utils import generate_token
from src.services.users.service import UserService
from src.db.database import get_sqlalchemy_session
from src.models.users.models import User


class TelegramService:
    @classmethod
    async def set_telegram_link_token(
        cls,
        user: User,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> str:
        token = generate_token()
        while await UserService().get_user(telegram_link_token=token, raise_exception=False, db=db):
            token = generate_token()
        user.telegram_link_token = token
        await db.commit()
        await db.refresh(user)
        return token

    @classmethod
    async def set_user_telegram_id(
        cls,
        token: str,
        telegram_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> dict:
        user: User = await UserService().get_user(telegram_link_token=token, db=db)
        if user.telegram_id:
            message = '❗️Вы уже подлючены к системе.'
        else:
            user.telegram_id = telegram_id
            await db.commit()
            await db.refresh(user)
            message = '☑️Вы успешно подключены к системе.'
        return {'message': message}

    @classmethod
    async def get_telegram_access_token(
        cls,
        telegram_id: int | str,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> dict:
        user: User = await UserService().get_user(telegram_id=telegram_id, db=db)
        if not user.telegram_id:
            raise UserHasNoTelegramLinked
        if user.telegram_id != telegram_id:
            raise UserHasNoAccess
        expire = datetime.utcnow() + timedelta(minutes=settings.TELEGRAM_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(data={'sub': str(user.id)}, expire=expire)
        return {'access_token': access_token}
