from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.templates.templates import TemplateService
from src.db.database import get_sqlalchemy_session
from src.models.users.models import User
from src.models.messages.models import Message
from src.schemas.users import (
    UserSchema,
    UserRegisterSchema,
    UserLoginSchema,
    RefreshTokenSchema
)
from src.services.auth.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    token_refresh
)
from src.services.users.dependencies import get_current_user
from src.services.users.service import UserService
from src.services.users.utils import register_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/register')
async def register(
    request: UserRegisterSchema,
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    user = await register_user(
        username=request.username,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
        db=db
    )
    access_token = await create_access_token({'sub': str(user.id)})
    refresh_token = await create_refresh_token(user=user, data={'sub': str(user.id)}, db=db)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/login')
async def login_user(
    request: UserLoginSchema,
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    user = await authenticate_user(
        username=request.username,
        password=request.password,
        db=db
    )
    access_token = await create_access_token(data={'sub': str(user.id)})
    refresh_token = await create_refresh_token(user=user, data={'sub': str(user.id)}, db=db)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/refresh')
async def refresh(
    request: RefreshTokenSchema,
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await token_refresh(refresh_token=request.refresh_token, db=db)
    return response


@router.get('/me', response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_sqlalchemy_session),
    current_user: User = Depends(get_current_user)
):
    user = await UserService.get_user(id=user_id, db=db)
    return user


@router.get('', response_model=list[UserSchema])
async def get_users(
    db: AsyncSession = Depends(get_sqlalchemy_session),
    current_user: User = Depends(get_current_user)
):
    user = await UserService.get_users(exclude_user=current_user, db=db)
    return user
