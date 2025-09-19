

# C:\Users\Computer\Desktop\python\Kiberded\main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TG_TOKEN


from database.engine import init_db
from handlers.start import start_router
from handlers.lessons import lessons_router
from handlers.generate_ai import generate_ai_router
from handlers.settings.choice_of_AI_model import settings_router


# Логирование (временно оставим INFO)
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(start_router)          # Роутер команды /start
    dp.include_router(settings_router)
    dp.include_router(lessons_router)        # Роутер уроков
    dp.include_router(generate_ai_router)    # Строка для подключения роутера генерации
    await init_db()


    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    # asyncio.run(main())
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")





# 
# import asyncio
# import logging
# from aiogram import Bot, Dispatcher
# from config import TG_TOKEN  # из config.py берём токен

# from handlers.start import start_router
# from handlers.generate_ai import generate_ai_router

# # Логирование (временно оставим INFO)
# logging.basicConfig(level=logging.INFO)

# async def main():
#     bot = Bot(token=TG_TOKEN)
#     dp = Dispatcher()
#     dp.include_router(start_router) # We register the start.router
#     # dp.include_router(generate_ai_router)

#     # Запускаем бота
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         print("Бот остановлен")
