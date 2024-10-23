import asyncio

import structlog
from aiogram.filters import Command

from src.telegram_bot.handlers.start import start_handler
from src.telegram_bot.base import bot, dp

logger = structlog.get_logger(__name__)


async def main():
    # handlers
    dp.message.register(start_handler, Command('start'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logger.info('bot started')
    asyncio.run(main())
