from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.services.messages.service import ChatService
from src.services.messages.utils import get_ws_current_user
from src.services.messages.manager import ConnectionManager, get_connection_manager
from src.services.users.service import UserService
from src.models.users.models import User

router = APIRouter(tags=['chat'])


@router.websocket('/chat/{receiver_id}')
async def chat_websocket(
    websocket: WebSocket,
    receiver_id: int,
    current_user: User = Depends(get_ws_current_user),
    manager: ConnectionManager = Depends(get_connection_manager),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    receiver = await UserService.get_user(id=receiver_id, db=db)
    await ChatService.chat_websocket(
        sender_id=current_user.id,
        sender_name=current_user.username,
        receiver_id=receiver_id,
        chat_id=receiver.telegram_chat_id,
        websocket=websocket,
        manager=manager,
        db=db
    )
