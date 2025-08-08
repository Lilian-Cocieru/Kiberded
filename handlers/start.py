

# C:\Users\Computer\Desktop\python\Kiberded\handlers\start.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.generate_ai import generate_ai_router
# Создаём роутер для start-команды
start_router = Router()

class Gen(StatesGroup):
    wait = State()

@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Hi! I am Kiberded, I am ready to help with my studies.")

@start_router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer("Wait, your request is generated")

@start_router.message()
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    response = await generate_ai_router(message.text)
    await message.answer(response)
    await state.clear()

    
