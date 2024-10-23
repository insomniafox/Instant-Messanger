from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.models.messages.models import Message


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
            .filter(
                ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
                ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
            )
            .order_by(Message.created_at)
        )
        return messages.scalars().all()

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
