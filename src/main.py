import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.redis import RedisStorage

from infrastructure.config import settings
from infrastructure.logging_config import setup_logging

from application.handlers import router


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting bot...")

    bot = Bot(token=settings.TELEGRAM_TOKEN)
    storage = RedisStorage.from_url(settings.REDIS_URL)

    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    try:
        logger.info("Bot polling started")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        logger.info("Shutting down bot...")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
