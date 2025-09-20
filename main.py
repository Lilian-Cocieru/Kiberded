

# C:\Users\Computer\Desktop\python\Kiberded\main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TG_TOKEN


from database.engine import init_db
from services.ai_models_sync import sync_ai_models
from handlers.start import start_router
from handlers.lessons import lessons_router
from handlers.generate_ai import generate_ai_router
from handlers.settings.choice_of_AI_model import settings_router



# Логирование (временно оставим INFO)
# logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(start_router)          # Роутер команды /start
    dp.include_router(settings_router)
    dp.include_router(lessons_router)        # Роутер уроков
    dp.include_router(generate_ai_router)    # Строка для подключения роутера генерации
    await init_db()                          # инициация бд
    await sync_ai_models()                   # синхронизация моделей перед стартом


    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
