

import asyncio

from aiogram import Bot, Dispatcher
from config import TG_TOKEN

from handlers.gen_handlers import gen_router
from handlers.user_handlers import user_router

async def main():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(gen_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)
    
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")