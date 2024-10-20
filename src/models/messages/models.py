
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Message(BaseModel):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sender = relationship('User', back_populates='sent_messages', foreign_keys=[sender_id])
    receiver = relationship('User', back_populates='received_messages', foreign_keys=[receiver_id])
