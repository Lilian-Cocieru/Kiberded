# C:\Users\Computer\Desktop\python\Kiberded\bot.py

import asyncio
from aiogram import Bot, Dispatcher
# Добавляем для логирования
import logging 
from config import TG_TOKEN
from database.engine import init_db #, engine, Base # engine, Base не нужны здесь

from handlers.start import start_router
from handlers.gen_handlers import gen_router

# Настраиваем базовое логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Получаем логгер для этого модуля

async def main():
    logger.info("Бот запускается...") # Добавили лог
    await init_db()
    logger.info("База данных инициализирована.") # Добавили лог

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start_router)
    dp.include_router(gen_router)
    logger.info("Роутеры включены: start_router и gen_router.") # Добавили лог

    logger.info("Бот готов к приему обновлений.") # Добавили лог
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")

# import asyncio

# from aiogram import Bot, Dispatcher
# from config import TG_TOKEN
# from database.engine import init_db, engine, Base

# from handlers.start import start_router
# from handlers.gen_handlers import gen_router



# async def main():

#     await init_db()

#     bot = Bot(token=TG_TOKEN)
#     dp = Dispatcher()
    
#     dp.include_router(start_router)
#     dp.include_router(gen_router)

#     await dp.start_polling(bot)
    
    
    
    
# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Выход")