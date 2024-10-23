from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.messages import MessageSchema
from src.db.database import get_sqlalchemy_session
from src.services.messages.messages import MessageService
from src.services.users.dependencies import get_current_user
from src.models.users.models import User


router = APIRouter(prefix='/messages', tags=['messages'])


@router.get("/message_history/{other_user_id}", response_model=list[MessageSchema])
async def get_chat_history(
    other_user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await MessageService.get_message_history(
        user_id=current_user.id,
        other_user_id=other_user_id,
        db=db
    )
    return response
