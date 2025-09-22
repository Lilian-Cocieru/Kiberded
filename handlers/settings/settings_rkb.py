# C:\Users\Computer\Desktop\python\Kiberded\handlers\settings\settings_rkb.py

from aiogram import Router, F
from aiogram.types import Message

from kb.reply_kb.menu_kb import main_menu, settings_menu, lessons_menu
from kb.inline_kb.models_ai_kb import build_models_keyboard


settings_rkb_router = Router()

@settings_rkb_router.message(F.text == "⚙️ Настройки")
async def open_settings(message: Message):
    """
    Открывает подменю Настройки.
    """
    await message.answer(
        "Настройки",
        reply_markup=settings_menu
    )

@settings_rkb_router.message(F.text == "🌐 Язык")
async def change_language(message: Message):
    """
    Заглушка для логики смены языка.
    """
    await message.answer("Здесь будет логика смены языка.")

@settings_rkb_router.message(F.text == "🤖 AI-модель")
async def change_ai_model(message: Message):
    """
    Заглушка для логики выбора AI-модели.
    """
    await message.answer("Аи модели", reply_markup=build_models_keyboard())





@settings_rkb_router.message(F.text == "💳 Подписка / Тариф")
async def change_subscription(message: Message):
    """
    Заглушка для логики подписки и тарифов.
    """
    await message.answer("Здесь будет логика подписки и тарифов.")

@settings_rkb_router.message(F.text == "⬅️ Назад")
async def back_to_main_menu(message: Message):
    """
    Возврат в главное меню.
    """
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu
    )