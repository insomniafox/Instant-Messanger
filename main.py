from fastapi import FastAPI, APIRouter

from src.api.users import router as users_router
from src.api.messages import router as messages_router
from src.api.telegram import router as telegram_router
from src.ws.chat import router as chat_router


app = FastAPI(
    title='Instant Messanger',
    description='Это реализация простого мессенджера на FastAPI.',
    version='0.0.1',
)

api_router = APIRouter(prefix='/api')
ws_router = APIRouter(prefix='/ws')

# HTTP
api_router.include_router(users_router)
api_router.include_router(messages_router)
api_router.include_router(telegram_router)

# WebSocket
ws_router.include_router(chat_router)

app.include_router(api_router)
app.include_router(ws_router)
