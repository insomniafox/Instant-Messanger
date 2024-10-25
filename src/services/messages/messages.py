from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.models.messages.models import Message
from src.models.users.models import User
from src.schemas.messages import MessageSchema


class MessageService:
    @classmethod
    async def get_messages(
        cls,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        **filters
    ) -> Sequence[Message]:
        result = await db.execute(select(Message).filter_by(**filters))
        return result.scalars().all()

    @classmethod
    async def get_message_history(
        cls,
        user_id: int,
        other_user_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session),
    ):
        messages = await db.execute(
            select(Message)
            .options(
                joinedload(Message.sender).load_only(User.username),  # Подгружаем username отправителя
                joinedload(Message.receiver).load_only(User.username)  # Подгружаем username получателя
            )
            .filter(
                ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
                ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
            )
            .order_by(Message.created_at)
        )
        return messages.scalars().all()

    @classmethod
    async def get_message_history_schema_response(
        cls,
        user_id: int,
        other_user_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session),
    ):
        messages = await cls.get_message_history(user_id, other_user_id, db)
        response = [
            MessageSchema(
                id=message.id,
                text=message.text,
                sender_id=message.sender_id,
                receiver_id=message.receiver_id,
                sender_username=message.sender.username,
                receiver_username=message.receiver.username,
                created_at=message.created_at,
                updated_at=message.updated_at
            )
            for message in messages
        ]
        return response

    @classmethod
    async def create_message(
        cls,
        text: str,
        sender_id: int,
        receiver_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> Message:
        message = Message(
            text=text,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message
