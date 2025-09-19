# C:\Users\Computer\Desktop\python\Kiberded\handlers\lessons.py
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from database.engine import SessionLocal
from database.lesson_crud import add_lesson

# Создаём роутер для обработчиков уроков
lessons_router = Router()

# Определяем состояния для FSM
class LessonStates(StatesGroup):
    title = State() # Состояние для получения названия урока
    summary = State() # Состояние для получения краткого содержания

@lessons_router.message(Command("add_lesson"))
async def add_lesson_handler(message: Message, state: FSMContext):
    """
    Обрабатывает команду /add_lesson и запускает FSM.
    """
    await message.answer("Отлично! Начнём. Пожалуйста, введите название урока:")
    await state.set_state(LessonStates.title)

@lessons_router.message(LessonStates.title)
async def process_lesson_title(message: Message, state: FSMContext):
    """
    Обрабатывает название урока и просит ввести краткое содержание.
    """
    if not message.text:
        await message.answer("Пожалуйста, введите название текстом.")
        return

    await state.update_data(title=message.text)
    await message.answer("Спасибо. Теперь введите краткое содержание урока:")
    await state.set_state(LessonStates.summary)

@lessons_router.message(LessonStates.summary)
async def process_lesson_summary(message: Message, state: FSMContext):
    """
    Обрабатывает краткое содержание, сохраняет данные и завершает FSM.
    """
    if not message.text:
        await message.answer("Пожалуйста, введите содержание текстом.")
        return

    user_data = await state.get_data()
    title = user_data.get('title')
    summary = message.text

    try:
        async with SessionLocal() as session:
            await add_lesson(
                session=session,
                user_id=message.from_user.id,
                title=title,
                summary=summary
            )
        await message.answer("Урок успешно сохранён!")
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении урока: {e}")
        # Логирование ошибки
        print(f"Ошибка сохранения урока: {e}")
    finally:
        # Важно: всегда завершайте состояние после выполнения
        await state.clear()
