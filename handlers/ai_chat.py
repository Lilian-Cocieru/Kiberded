# C:\Users\Computer\Desktop\python\Kiberded\handlers\ai_chat.py
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import SessionLocal
from database.models import User
from config import ALL_MODELS, OR_API_KEY
import httpx  # Для запросов к OpenRouter API

ai_router = Router()

# -------------------
# Основной обработчик сообщений для AI
# -------------------
@ai_router.message()
async def ai_message_handler(message: Message):
    """
    Принимает текст пользователя и отправляет его в выбранную LLM.
    """
    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user or not user.ai_model_id:
            await message.answer("Сначала выберите AI-модель через /models.")
            return

        # Получаем модель пользователя
        model_info = next((m for m in ALL_MODELS if m["id"] == user.ai_model_id), None)
        if not model_info:
            await message.answer("Выбранная модель недоступна. Пожалуйста, выберите снова.")
            return

        await message.answer("Обрабатываю ваш запрос... ⏳")

        # Пример запроса к OpenRouter (GPT-4o, Qwen и др.)
        # Здесь можно подставить любую другую LLM API
        payload = {
            "model": model_info["model_code"],
            "input": message.text
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                headers = {"Authorization": f"Bearer {OR_API_KEY}"}
                response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                # Предположим, что ответ в data['output'][0]['content']
                ai_text = data.get("output", [{}])[0].get("content", "Модель не вернула ответ.")

            await message.answer(ai_text)
        except Exception as e:
            await message.answer(f"Ошибка при обращении к AI: {e}")
            print(f"AI запрос ошибка: {e}")
