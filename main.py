"""
BITU qabul boti — kirish nuqtasi.

Botni ishga tushirish:
    python main.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database import Database
from handlers import admin, registration, start
from middlewares import RateLimitMiddleware

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, db: Database) -> None:
    """Bot ishga tushganda chaqiriladi."""
    await db.init()
    bot_info = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s (id=%s)", bot_info.username, bot_info.id)


async def on_shutdown(db: Database) -> None:
    """Bot to'xtatilganda chaqiriladi."""
    await db.close()
    logger.info("Bot to'xtatildi")


async def main() -> None:
    # Konfiguratsiya va loglarni sozlash
    config.setup_logging()
    config.validate_config()

    # Bot va Dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Ma'lumotlar bazasi
    db = Database(config.DATABASE_PATH)

    # Middleware — rate limiting
    rate_limiter = RateLimitMiddleware(
        max_messages=config.RATE_LIMIT_MAX,
        window_seconds=config.RATE_LIMIT_WINDOW,
    )
    dp.message.middleware(rate_limiter)
    dp.callback_query.middleware(rate_limiter)

    # db obyektini handlerlarga uzatish uchun
    dp["db"] = db

    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(admin.router)

    # Startup/shutdown hooklari
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, db=db)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot foydalanuvchi tomonidan to'xtatildi")
