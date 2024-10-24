import structlog
from typing import Optional

from src.celery_tasks.celery import celery_app

from src.telegram_bot.notifications.notifications import send_message_notification

logger = structlog.get_logger(__name__)


@celery_app.task()
def send_message_notification_task(
    sender_name: str,
    chat_id: int | None
):
    if not chat_id:
        logger.info('Chat id was not provided.')
        return
    send_message_notification(sender_name, chat_id)
