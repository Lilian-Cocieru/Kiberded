
# C:\Users\Computer\Desktop\python\Kiberded\handlers\start.py

# C:\Users\Computer\Desktop\python\Kiberded\handlers\start.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy import select

from database.engine import SessionLocal
from database.models import User
from kb.reply_kb.menu_kb import main_menu


# Создаём роутер для start-команды
start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message):
    """
    Обрабатывает команду /start и сохраняет пользователя в БД.
    """
    async with SessionLocal() as session:
        # Проверяем, существует ли пользователь с таким ID
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            # Если пользователь не найден, создаём новую запись
            new_user = User(
                tg_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name
            )
            session.add(new_user)
            await session.commit()
            greeting = "Привет! Я Kiberded, и я готов помочь с учёбой."
        else:
            greeting = "С возвращением! 👋 Я снова готов помочь с учёбой."

    # Показываем меню
    await message.answer(
        f"{greeting}",
        reply_markup=main_menu
    )

