import structlog
from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.messages.manager import ConnectionManager, get_connection_manager
from src.services.messages.messages import MessageService
from src.db.database import get_sqlalchemy_session

logger = structlog.get_logger(__name__)


class ChatService:
    @classmethod
    async def chat_websocket(
        cls,
        sender_id: int,
        receiver_id: int,
        sender_name: str,
        chat_id: int | None,
        websocket: WebSocket,
        manager: ConnectionManager = Depends(get_connection_manager),
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ):
        await manager.connect(websocket, sender_id)
        try:
            while True:
                data = await websocket.receive_text()
                await MessageService.create_message(
                    text=data,
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    db=db
                )
                await manager.send_personal_message(  # Отправка получателю
                    f'User {receiver_id}: {data}',
                    receiver_id,
                    sender_name,
                    chat_id
                )
        except WebSocketDisconnect:
            await manager.disconnect(user_id=sender_id)
            logger.info('Connection closed.')
