from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.db.database import get_sqlalchemy_session
from src.services.auth.exceptions import (
    InvalidTokenException,
    NotAuthorizedException
)

from src.models.users.models import User
from src.services.auth.utils import ACCESS_TYPE, decode_token
from src.services.users.service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> User:
    payload = decode_token(token)

    token_type = payload.get("type")
    if token_type != ACCESS_TYPE:
        raise InvalidTokenException

    user_id = payload.get("sub")
    if not user_id:
        raise NotAuthorizedException

    user = await UserService.get_user(id=int(user_id), db=db)
    return user
