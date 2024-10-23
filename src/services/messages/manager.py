from typing import Optional

from fastapi import WebSocket

from src.celery_tasks.tasks import send_message_notification_task


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(
        self,
        message: str,
        user_id: int,
        sender_name: str,
        chat_id: Optional[int] = None
    ):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)
        else:
            send_message_notification_task.delay(sender_name, chat_id)

    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)


async def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()
