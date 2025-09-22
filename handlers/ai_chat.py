
# C:\Users\Computer\Desktop\python\Kiberded\handlers\ai_chat.py

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import SessionLocal
from database.models import User
from config import OR_API_KEY, FREE_MODELS
import httpx

ai_router = Router()

# -------------------
# Основной обработчик сообщений для AI
# -------------------
@ai_router.message()
async def ai_message_handler(message: Message):
    """
    Эта функция-обработчик будет вызвана каждый раз, когда пользователь
    отправляет любое текстовое сообщение (так как у нас нет фильтра
    по тексту, кроме тех, что в других роутерах).
    """

    # --- Подключение к базе данных ---
    # Это асинхронный способ работы с базой данных (SQLite).
    # 'async with' гарантирует, что сессия будет закрыта автоматически
    # после выполнения всех операций.
    async with SessionLocal() as session:
        # --- Получение данных пользователя из БД ---
        # Мы ищем пользователя по его Telegram ID.
        # Это позволяет нам узнать, какую модель ИИ он выбрал ранее.
        user = await session.get(User, message.from_user.id)
        
        # --- Проверка на существование пользователя и выбранной модели ---
        # Если пользователь не найден в БД или он ещё не выбрал модель,
        # мы просим его это сделать и прерываем выполнение функции.
        if not user or not user.ai_model_id:
            await message.answer("Сначала выберите AI-модель.")
            return

        # --- Поиск информации о выбранной модели ---
        # Мы ищем в списке 'FREE_MODELS' ту модель,
        # ID которой сохранен в базе данных для текущего пользователя.
        model_info = next((m for m in FREE_MODELS if m["id"] == user.ai_model_id), None)
        
        # --- Проверка на доступность модели ---
        # Если модель с таким ID не найдена в нашем списке,
        # мы сообщаем об этом пользователю.
        if not model_info:
            await message.answer("Выбранная модель недоступна. Пожалуйста, выберите снова.")
            return

        # --- Уведомление пользователя ---
        # Отправляем сообщение, чтобы пользователь знал,
        # что его запрос обрабатывается.
        await message.answer("Обрабатываю ваш запрос... ⏳")

        # --- Формирование запроса к API OpenRouter ---
        # Это самая важная часть, которую мы исправляли.
        # OpenRouter ожидает, что вы отправите список сообщений.
        # Ключевой формат: 'messages', который содержит список словарей,
        # где каждый словарь - это сообщение с 'role' (ролью) и 'content' (содержимым).
        payload = {
            "model": model_info["model_code"],
            "messages": [
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        }
        
        # --- Отправка запроса ---
        # Используем httpx для отправки асинхронного запроса.
        # 'timeout' устанавливает максимальное время ожидания ответа.
        # В 'headers' мы передаем ключ авторизации, который нужен API.
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                headers = {"Authorization": f"Bearer {OR_API_KEY}"}
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                # Если HTTP-статус ответа не 2xx, будет вызвано исключение.
                response.raise_for_status()
                data = response.json()
                
                # --- Извлечение ответа от AI ---
                # OpenRouter возвращает ответ в формате, похожем на OpenAI.
                # Мы извлекаем текст из ответа, используя безопасный метод '.get()',
                # чтобы избежать ошибок, если какой-то ключ отсутствует.
                # Путь к ответу: data['choices'][0]['message']['content'].
                ai_text = data.get("choices", [{}])[0].get("message", {}).get("content", "Модель не вернула ответ.")

            # --- Отправка ответа пользователю ---
            # Отправляем сгенерированный текст обратно в Telegram.
            await message.answer(ai_text)
        
        # --- Обработка ошибок ---
        # Если при запросе к API произошла какая-либо ошибка,
        # мы сообщаем об этом пользователю и выводим ошибку в консоль.
        except Exception as e:
            await message.answer(f"Ошибка при обращении к AI: {e}")
            print(f"AI запрос ошибка: {e}")









# # C:\Users\Computer\Desktop\python\Kiberded\handlers\ai_chat.py
# from aiogram import Router
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# from sqlalchemy.ext.asyncio import AsyncSession
# from database.engine import SessionLocal
# from database.models import User
# from config import OR_API_KEY, FREE_MODELS  # , ALL_MODELS
# import httpx  # Для запросов к OpenRouter API

# ai_router = Router()

# # -------------------
# # Основной обработчик сообщений для AI
# # -------------------
# @ai_router.message()
# async def ai_message_handler(message: Message):
#     """
#     Принимает текст пользователя и отправляет его в выбранную LLM.
#     """
#     async with SessionLocal() as session:
#         user = await session.get(User, message.from_user.id)
#         if not user or not user.ai_model_id:
#             await message.answer("Сначала выберите AI-модель через /models.")
#             return

#         # Получаем модель пользователя
#         model_info = next((m for m in FREE_MODELS if m["id"] == user.ai_model_id), None)
#         if not model_info:
#             await message.answer("Выбранная модель недоступна. Пожалуйста, выберите снова.")
#             return

#         await message.answer("Обрабатываю ваш запрос... ⏳")

#         # Пример запроса к OpenRouter (GPT-4o, Qwen и др.)
#         # Здесь можно подставить любую другую LLM API
#         payload = {
#             "model": model_info["model_code"],
#             "input": message.text
#         }

#         try:
#             async with httpx.AsyncClient(timeout=30) as client:
#                 headers = {"Authorization": f"Bearer {OR_API_KEY}"}
#                 response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
#                 response.raise_for_status()
#                 data = response.json()
#                 # Предположим, что ответ в data['output'][0]['content']
#                 ai_text = data.get("output", [{}])[0].get("content", "Модель не вернула ответ.")

#             await message.answer(ai_text)
#         except Exception as e:
#             await message.answer(f"Ошибка при обращении к AI: {e}")
#             print(f"AI запрос ошибка: {e}")
