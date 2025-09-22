# C:\Users\Computer\Desktop\python\Kiberded\handlers\settings\choice_of_AI_model.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.engine import SessionLocal
from database.models import User

# Импортируем функцию, которая строит клавиатуру
from kb.inline_kb.models_ai_kb import build_models_keyboard
from config import FREE_MODELS  # , ALL_MODELS

# Создаём роутер для настроек
settings_router = Router()

@settings_router.message(Command("models"))
async def show_models_handler(message: Message):
    """
    Обрабатывает команду /models и отображает список моделей.
    """
    keyboard = build_models_keyboard()
    await message.answer("Выберите AI-модель для общения:", reply_markup=keyboard)



from sqlalchemy import select

@settings_router.callback_query(F.data.startswith("select_model:"))
async def select_model_callback(callback: CallbackQuery):
    model_id = int(callback.data.split(":")[1])

    async with SessionLocal() as session:
        try:
            result = await session.execute(select(User).where(User.tg_id == callback.from_user.id))
            user = result.scalar_one_or_none()

            if not user:
                await callback.answer("Произошла ошибка. Попробуйте снова.", show_alert=True)
                return

            user.ai_model_id = model_id
            await session.commit()

            selected_model_name = next((m['name'] for m in FREE_MODELS if m['id'] == model_id), 'Неизвестная модель')

            await callback.message.edit_text(
                f"Вы выбрали модель **{selected_model_name}**.",
                reply_markup=None
            )
            await callback.answer()
        except Exception as e:
            print(f"Ошибка при выборе модели: {e}")
            await callback.answer(f"Произошла ошибка: {e}", show_alert=True)
