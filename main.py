import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

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
        logger.info("🚀 Запуск бота на Replit...")
        
        # Проверка токена
        if not Config.BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен! Проверьте Secrets в Replit")
            return
        
        # Инициализация бота
        bot = Bot(token=Config.BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Регистрация роутеров
        dp.include_router(start_router)
        dp.include_router(catalog_router)
        dp.include_router(cart_router)
        dp.include_router(order_router)

        # Удаляем webhook
        await bot.delete_webhook(drop_pending_updates=True)
        
        logger.info("✅ Бот запущен и готов к работе!")
        logger.info("📱 Отправьте /start боту в Telegram")
        
        # Запускаем поллинг
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
