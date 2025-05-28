from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! Напишите свой запрос.')