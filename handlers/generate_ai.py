# C:\Users\Computer\Desktop\python\Kiberded\handlers\generate_ai.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from llama_index.core.query_engine import BaseQueryEngine
from openai import AsyncOpenAI
from sqlalchemy import select
import re


from config import OR_API_KEY, ALL_MODELS
from handlers.utils import send_long_message
from database.data_loader import create_and_save_index
from database.engine import SessionLocal
from database.models import User

# Создаём роутер для обработки AI-запросов
generate_ai_router = Router()

# Создаём состояния для FSM
class Gen(StatesGroup):
    wait = State()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OR_API_KEY,
)


def escape_markdown(text: str) -> str:
    """
    Экранируем специальные символы MarkdownV2, чтобы Telegram не ругался.
    """
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


async def generate_response_from_ai(text: str, model_code: str):
    """
    Асинхронная функция для обращения к API OpenRouter и получения ответа.
    """
    completion = await client.chat.completions.create(
        model=model_code,  # Используем модель, переданную в аргументах
        messages=[
            {
                "role": "user",
                "content": text
            }
        ]
    )
    print(completion)
    return completion.choices[0].message.content


@generate_ai_router.message(F.text)
async def generating(message: Message, state: FSMContext):
    """
    Обработчик для всех текстовых сообщений.
    """
    current_state = await state.get_state()
    
    if current_state == Gen.wait:
        await message.answer("Please wait, your previous request is still processed.")
        return

    await state.set_state(Gen.wait)
    await message.answer("I generate the answer ... Please wait.")

    response: str = ""
    query_engine: BaseQueryEngine = None
    
    try:
        # Получаем выбранную пользователем модель из БД
        async with SessionLocal() as session:
            stmt = select(User).where(User.tg_id == message.from_user.id)
            result = await session.execute(stmt)
            user_in_db = result.scalar_one_or_none()
            # user_in_db = await session.get(User, message.from_user.id)
            if not user_in_db or not user_in_db.ai_model_id:
                await message.answer("Пожалуйста, сначала выберите AI-модель командой.")
                await state.clear()
                return
            
            # Находим код модели по ID, используя наш список ALL_MODELS
            selected_model_code = next((model['model_code'] for model in ALL_MODELS if model['id'] == user_in_db.ai_model_id), None)
            
            if not selected_model_code:
                await message.answer("Произошла ошибка при выборе модели. Пожалуйста, выберите её снова.")
                await state.clear()
                return

        # Проверяем, если запрос связан с "уроками" или "задачами".
        if "lessons" in message.text.lower() or "tasks" in message.text.lower():
            index = await create_and_save_index(user_id=message.from_user.id)
            if index:
                query_engine = index.as_query_engine()

        if query_engine:
            response = await query_engine.query(message.text)
        else:
            response = await generate_response_from_ai(message.text, model_code=selected_model_code)
            
        await send_long_message(message, escape_markdown(response))

        # await send_long_message(message, response)
        # await send_long_message(message, response.response)
        
    except Exception as e:
        await message.answer(f"Произошла ошибка при генерации ответа: {e}")
        print(f"Ошибка в AI-обработчике: {e}")
        
    finally:
        await state.clear()







# @generate_ai_router.message(F.text)
# async def generating(message: Message, state: FSMContext):
#     """
#     Обработчик для всех текстовых сообщений.
#     Управляет состоянием в одном месте.
#     """
#     # 🌟 НОВОЕ: Проверяем текущее состояние FSM.
#     current_state = await state.get_state()
    
#     # Если бот уже в состоянии "ожидания", сообщаем об этом и выходим.
#     if current_state == Gen.wait:
#         await message.answer("Пожалуйста, подождите, ваш предыдущий запрос ещё обрабатывается.")
#         return # Завершаем выполнение функции

#     # Если состояние None (т.е., бот свободен), начинаем генерацию.
#     await state.set_state(Gen.wait)
#     await message.answer("Генерирую ответ... Пожалуйста, подождите.")

#     try:
#         response = await generate_response_from_ai(message.text)
#         await send_long_message(message, response)
#     finally:
#         await state.clear()


# 🌟 ИСПРАВЛЕНИЕ: Используем F.state.ne(Gen.wait) вместо ~Gen.wait
# @generate_ai_router.message(F.text, F.state.ne(Gen.wait))
# 🌟 ИСПРАВЛЕНИЕ: Проверяем, что состояние равно None
# @generate_ai_router.message(F.text, F.state == None)
# async def generating(message: Message, state: FSMContext):
#     """
#     Обработчик текстовых сообщений, когда бот не в состоянии "ожидания".
#     """
#     # 🌟 Устанавливаем состояние "ожидания"
#     await state.set_state(Gen.wait)

#     # Отправляем пользователю сообщение о начале генерации
#     await message.answer("Generating your response... Please wait.")

#     try:
#         # 🌟 Вызываем функцию для получения ответа от AI
#         response = await generate_response_from_ai(message.text)
#         # Отправляем длинный ответ
#         await send_long_message(message, response)
#     finally:
#         # 🌟 Обязательно очищаем состояние, даже если произошла ошибка
#         await state.clear()




# @generate_ai_router.message(Gen.wait)
# async def stop_flood(message: Message):
#     """
#     🌟 Обработчик, который срабатывает, если пользователь отправил новое сообщение
#     во время генерации предыдущего ответа.
#     """
#     await message.answer("Please wait, your previous request is still being processed.")




# # C:\Users\Computer\Desktop\python\Kiberded\handlers\generate_ai.py

# # C:\Users\Computer\Desktop\python\Kiberded\handlers\generate_ai.py

# from aiogram import Router, F
# from aiogram.types import Message
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext

# from openai import AsyncOpenAI
# from config import OR_API_KEY
# from handlers.utils import send_long_message

# # Создаём роутер для обработки AI-запросов
# generate_ai_router = Router()

# # Создаём состояния для FSM
# class Gen(StatesGroup):
#     wait = State()

# client = AsyncOpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OR_API_KEY,
# )

# async def generate_response_from_ai(text: str):
#     """
#     Асинхронная функция для обращения к API OpenRouter и получения ответа.
#     Вынесена из обработчика для чистоты кода.
#     """
#     completion = await client.chat.completions.create(
#         model="openai/gpt-oss-20b:free",
#         messages=[
#             {
#                 "role": "user",
#                 "content": text
#             }
#         ]
#     )
#     print(completion)
#     return completion.choices[0].message.content

# # 🌟 ИСПРАВЛЕНИЕ: Используем F.state.ne(Gen.wait) вместо ~Gen.wait
# # @generate_ai_router.message(F.text, F.state.ne(Gen.wait))
# @generate_ai_router.message(F.text)
# async def generating(message: Message, state: FSMContext):
#     """
#     Обработчик текстовых сообщений, когда бот не в состоянии "ожидания".
#     """
#     # 🌟 Устанавливаем состояние "ожидания"
#     await state.set_state(Gen.wait)

#     # Отправляем пользователю сообщение о начале генерации
#     await message.answer("Generating your response... Please wait.")

#     try:
#         # 🌟 Вызываем функцию для получения ответа от AI
#         response = await generate_response_from_ai(message.text)
#         # Отправляем длинный ответ
#         await send_long_message(message, response)
#     finally:
#         # 🌟 Обязательно очищаем состояние, даже если произошла ошибка
#         await state.clear()

# @generate_ai_router.message(Gen.wait)
# async def stop_flood(message: Message):
#     """
#     🌟 Обработчик, который срабатывает, если пользователь отправил новое сообщение
#     во время генерации предыдущего ответа.
#     """
#     await message.answer("Please wait, your previous request is still being processed.")






# Изначальный файл

# from openai import AsyncOpenAI

# from config import OR_API_KEY




# client = AsyncOpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=OR_API_KEY,
# )



# async def generate_ai_router(text: str):
#   completion = await client.chat.completions.create(
#     model="openai/gpt-oss-20b:free",
#       messages=[
#         {
#           "role": "user",
#           "content": text
#         }
#       ]
#   )
#   print(completion)
#   return completion.choices[0].message.content
