import logging
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import exceptions, Router

from .texts import *
from domain.services.agent_service import AgentService
from infrastructure.ai.gigachain_client import GigaChainClient


logger = logging.getLogger(__name__)

router = Router()

llm_client = GigaChainClient()
agent_service = AgentService(llm_client)

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(WELCOME_MESSAGE)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(HELP_MESSAGE)

@router.message()
async def all_messages_handler(message: Message):
    """
    Обработчик любых других текстовых сообщений. 
    Вызываем agent_service.handle_user_message и шлём ответ обратно.
    """
    telegram_id = message.from_user.id
    text = message.text.strip()

    logger.info(f"Received message from {telegram_id}: {text!r}")

    try:
        response_text = await agent_service.handle_user_message(
            telegram_id=telegram_id,
            text=text
        )
        await message.answer(response_text)

    except Exception as e:
        logger.exception(f"Error in handling message: {e}")
        try:
            await message.answer("Произошла ошибка сервера. Попробуйте позже.")

        except exceptions.BotBlocked:
            logger.warning(f"Cannot send message to user {telegram_id}: Bot blocked.")
