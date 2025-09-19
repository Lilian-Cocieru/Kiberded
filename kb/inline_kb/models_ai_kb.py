# C:\Users\Computer\Desktop\python\Kiberded\kb\inline_kb\models_ai_kb.py
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import ALL_MODELS

def build_models_keyboard():
    """
    Создаёт инлайн-клавиатуру с кнопками для каждой модели из списка.
    """
    builder = InlineKeyboardBuilder()
    for model in ALL_MODELS:
        # data содержит уникальный ID модели, который добавили в словарь
        builder.button(text=model["name"], callback_data=f"select_model:{model['id']}")
    builder.adjust(2)  # Отображаем по 2 кнопки в ряд
    return builder.as_markup()
