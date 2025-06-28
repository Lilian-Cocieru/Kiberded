

import asyncio

from aiogram import Bot, Dispatcher
from config import TG_TOKEN
from database.engine import init_db, engine, Base
from handlers.gen_handlers import gen
from handlers.start import user_router




async def main():

    await init_db()

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(gen)
    dp.include_router(user_router)
    
    await dp.start_polling(bot)
    
    
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")