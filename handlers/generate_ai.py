

# C:\Users\Computer\Desktop\python\Kiberded\handlers\generate_ai.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from llama_index.core.query_engine import BaseQueryEngine


from openai import AsyncOpenAI


from config import OR_API_KEY
from handlers.utils import send_long_message
from database.data_loader import create_and_save_index



# Создаём роутер для обработки AI-запросов
generate_ai_router = Router()

# Создаём состояния для FSM
class Gen(StatesGroup):
    wait = State()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OR_API_KEY,
)

async def generate_response_from_ai(text: str):
    """
    Асинхронная функция для обращения к API OpenRouter и получения ответа.
    Вынесена из обработчика для чистоты кода.
    """
    completion = await client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
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
    Управляет состоянием и решает, использовать ли RAG.
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
        # Проверяем, если запрос связан с "уроками" или "задачами".
        if "lessons" in message.text.lower() or "tasks" in message.text.lower():
            # Создаём движок запросов на основе данных пользователя (RAG)
            index = await create_and_save_index(user_id=message.from_user.id)
            if index:
                query_engine = index.as_query_engine()
        
        if query_engine:
            # Если движок RAG создан, используем его
            response = await query_engine.query(message.text)
        else:
            # Иначе используем обычную генерацию
            response = await generate_response_from_ai(message.text)
            
        await send_long_message(message, response)
        
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
