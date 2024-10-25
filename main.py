from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.templates import *
from src.api.users import router as users_router
from src.api.messages import router as messages_router
from src.api.telegram import router as telegram_router
from src.api.chat_templates import router as template_router
from src.ws.chat import router as chat_router


app = FastAPI(
    title='Instant Messanger',
    description='Это реализация простого мессенджера на FastAPI.',
    version='0.0.1',
)

app.mount('/static', StaticFiles(directory='src/static'), name='static')

api_router = APIRouter(prefix='/api')
ws_router = APIRouter(prefix='/ws')

# HTTP
api_router.include_router(users_router)
api_router.include_router(messages_router)
api_router.include_router(telegram_router)

# WebSocket
ws_router.include_router(chat_router)

app.include_router(template_router)  # templates
app.include_router(api_router)
app.include_router(ws_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/chat")

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Вы можете указать конкретные домены, например ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)
