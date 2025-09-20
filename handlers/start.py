
# C:\Users\Computer\Desktop\python\Kiberded\handlers\start.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy import select

from database.engine import SessionLocal
from database.models import User
from kb.inline_kb.models_ai_kb import build_models_keyboard


# Создаём роутер для start-команды
start_router = Router()

@start_router.message(CommandStart())
async def start_handler(message: Message):
    """
    Обрабатывает команду /start и сохраняет пользователя в БД.
    """
    async with SessionLocal() as session:
        # Проверяем, существует ли пользователь с таким ID
        existing_user = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = existing_user.scalar_one_or_none()

        if user is None:
            # Если пользователь не найден, создаём новую запись
            new_user = User(
                tg_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name
            )
            session.add(new_user)
            await session.commit()
            await message.answer("Привет! Я Kiberded, и я готов помочь с учёбой. Вы были добавлены в базу данных.")
        else:
            # Если пользователь уже существует, просто приветствуем его
            await message.answer("С возвращением! Я готов помочь с учёбой.")
    
    # Отправляем клавиатуру с выбором моделей после приветствия
    models_keyboard = build_models_keyboard()
    await message.answer("Для начала, пожалуйста, выберите AI-модель для работы:", reply_markup=models_keyboard)
