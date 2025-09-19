# C:\Users\Computer\Desktop\python\Kiberded\handlers\settings\choice_of_AI_model.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import SessionLocal
from database.models import User

# Импортируем функцию, которая строит клавиатуру, из вашего файла
from kb.inline_kb.models_ai_kb import build_models_keyboard
from config import ALL_MODELS

# Создаём роутер для настроек
settings_router = Router()

@settings_router.message(Command("models"))
async def show_models_handler(message: Message):
    """
    Обрабатывает команду /models и отображает список моделей.
    """
    keyboard = build_models_keyboard()
    await message.answer("Выберите AI-модель для общения:", reply_markup=keyboard)


@settings_router.callback_query(F.data.startswith("select_model:"))
async def select_model_callback(callback: CallbackQuery):
    """
    Обрабатывает нажатие на кнопку выбора модели.
    """
    model_id = int(callback.data.split(":")[1])

    async with SessionLocal() as session:
        try:
            user = await session.get(User, callback.from_user.id)
            
            if not user:
                await callback.answer("Произошла ошибка. Попробуйте снова.")
                return

            user.ai_model_id = model_id
            await session.commit()
            
            selected_model_name = next((model['name'] for model in ALL_MODELS if model['id'] == model_id), 'Неизвестная модель')

            await callback.message.edit_text(
                f"Вы выбрали модель **{selected_model_name}**.",
                reply_markup=None
            )
        except Exception as e:
            await callback.answer(f"Произошла ошибка: {e}")
            print(f"Ошибка при выборе модели: {e}")
        finally:
            await callback.answer()