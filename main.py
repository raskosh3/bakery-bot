import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Config
from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.cart import router as cart_router
from handlers.order import router as order_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info("🚀 Запуск бота на Railway...")

        # Проверка токена
        if not Config.BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен!")
            return

        # Инициализация бота
        bot = Bot(
            token=Config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Регистрация роутеров
        dp.include_router(start_router)
        dp.include_router(catalog_router)
        dp.include_router(cart_router)
        dp.include_router(order_router)

        # Удаляем webhook (используем polling)
        await bot.delete_webhook(drop_pending_updates=True)

        logger.info("✅ Бот запущен и готов к работе!")
        logger.info(f"🤖 Бот: @{(await bot.get_me()).username}")

        # Запускаем поллинг
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        if 'bot' in locals():
            await bot.session.close()


if __name__ == "__main__":
    # Проверяем обязательные переменные
    required_vars = ['BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Отсутствуют переменные: {missing_vars}")
        sys.exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")