# C:\Users\Computer\Desktop\python\Kiberded\handlers\settings\settings_ikb.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from kb.inline_kb.models_ai_kb import build_models_keyboard  # функция для создания inline клавиатуры

settings_ikb_router = Router()

# Для inline-кнопки, которая открывает выбор модели
@settings_ikb_router.callback_query(F.data == "🤖 AI-модель")
async def open_ai_models(callback: CallbackQuery):
    """
    Открывает меню выбора AI-модели по callback.
    """
    models_keyboard = build_models_keyboard()
    await callback.message.edit_text(
        "Для начала, пожалуйста, выберите AI-модель для работы:",
        reply_markup=models_keyboard
    )
    await callback.answer()  # закрываем "часики" на кнопке
