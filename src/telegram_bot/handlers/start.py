import structlog
from aiogram.filters import CommandObject
from aiogram.types import Message

from src.telegram_bot.api_client.messanger_client import MessangerAPIClient
from src.telegram_bot.api_client.exceptions import MessangerAPIException

logger = structlog.get_logger(__name__)


async def start_handler(message: Message, command: CommandObject):
    token = command.args
    if not token:
        await message.reply("Что-то пошло не так. Попробуйте еще раз.")
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        response = await MessangerAPIClient.link_telegram_id(token, user_id, chat_id)
        await message.reply(response.get('message'))
    except MessangerAPIException as e:
        logger.error('Error occurred!', error=str(e))
        await message.reply("Что-то пошло не так. Попробуйте снова позже.")
