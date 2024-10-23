from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from src.core.config import settings
from src.services.auth.exceptions import (
    TokenExpiredException,
    InvalidTokenException,
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

REFRESH_TYPE = 'refresh'
ACCESS_TYPE = 'access'


def create_jwt_token(
    data: dict,
    token_type: str,
    expire: Optional[datetime] = None
) -> str:
    if not expire:
        expire_days = (
            settings.ACCESS_TOKEN_EXPIRE_DAYS
            if token_type == ACCESS_TYPE
            else settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        expire = datetime.utcnow() + timedelta(days=expire_days)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise InvalidTokenException
    return payload
