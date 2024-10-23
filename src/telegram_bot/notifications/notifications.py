import structlog

from src.telegram_bot.base import bot

logger = structlog.get_logger(__name__)


def send_message_notification(
    sender_name: str,
    chat_id: int
):
    message = f'Пользователь {sender_name} прислал вам сообщение.'
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.send_message(chat_id, message))
    except Exception as e:
        logger.error('Error occurred!', error=str(e))
