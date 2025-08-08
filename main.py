

# C:\Users\Computer\Desktop\python\Kiberded\main.py

# main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TG_TOKEN  # из config.py берём токен
# import start-royter
from handlers.start import start_router
from handlers.generate_ai import generate_ai_router

# Логирование (временно оставим INFO)
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(start_router) # We register the start.router
    # dp.include_router(generate_ai_router)

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")

