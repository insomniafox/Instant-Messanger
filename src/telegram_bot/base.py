from aiogram import Dispatcher, Bot

from src.core.config import settings


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
