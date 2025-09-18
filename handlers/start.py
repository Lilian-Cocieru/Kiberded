

# C:\Users\Computer\Desktop\python\Kiberded\handlers\start.py

# 🌟 ИСПРАВЛЕНИЕ: Убраны все импорты и обработчики, не относящиеся к команде /start.

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

# Создаём роутер для start-команды
start_router = Router()

@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Hi! I am Kiberded, I am ready to help with my studies.")

























# from aiogram import Router, F
# from aiogram.types import Message
# from aiogram.filters import CommandStart
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext


# from handlers.generate_ai import generate_ai_router
# from handlers.utils import send_long_message


# # Создаём роутер для start-команды
# start_router = Router()


# class Gen(StatesGroup):
#     wait = State()


# @start_router.message(CommandStart())  # Ответ на команду /start
# async def start_handler(message: Message):
#     await message.answer("Hi! I am Kiberded, I am ready to help with my studies.")


# @start_router.message(Gen.wait)        # Ответ на сообщение во время генерации запроса
# async def stop_flood(message: Message):
#     await message.answer("Wait, your request is generated")


# @start_router.message()   # Генерация ответа ИИ, и разбивка на отделиные файлы длинее 4096 символов
# async def generating(message: Message, state: FSMContext):
#     await state.set_state(Gen.wait)
#     response = await generate_ai_router(message.text)
    
#     # Используем функцию для отправки длинного ответа
#     await send_long_message(message, response)
    
#     await state.clear()
    