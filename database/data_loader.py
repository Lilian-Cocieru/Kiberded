
# C:\Users\Computer\Desktop\python\Kiberded\database\data_loader.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from llama_index.core import VectorStoreIndex, Document
from llama_index.core.embeddings import resolve_embed_model

from database.engine import SessionLocal
from database.models import Lesson, Task, User
from config import DEFAULT_EMBED_MODEL
async def get_user_data_for_rag(session: AsyncSession, user_id: int):
    """
    Асинхронно извлекает уроки и задачи конкретного пользователя
    из базы данных и форматирует их.
    """
    # Запрос для получения уроков пользователя
    lessons_query = select(Lesson).where(Lesson.user_id == user_id)
    lessons_result = await session.execute(lessons_query)
    lessons = lessons_result.scalars().all()

    # Запрос для получения задач пользователя
    tasks_query = select(Task).where(Task.user_id == user_id)
    tasks_result = await session.execute(tasks_query)
    tasks = tasks_result.scalars().all()

    formatted_data = []

    # Форматируем уроки
    for lesson in lessons:
        formatted_data.append(f"Урок: {lesson.title}. Краткое содержание: {lesson.summary}")

    # Форматируем задачи
    for task in tasks:
        formatted_data.append(f"Задача: {task.subject}. Описание: {task.description}. Ответ: {task.answer}")

    return formatted_data

async def create_and_save_index(user_id: int):
    """
    Создает индекс на основе данных пользователя и сохраняет его.
    """
    try:
        async with SessionLocal() as session:
            # Получаем данные пользователя из БД
            user_data = await get_user_data_for_rag(session, user_id)
            
            if not user_data:
                print("Данные пользователя не найдены. Индекс не будет создан.")
                return None

            # Создаем объекты Document для LlamaIndex
            documents = [Document(text=text) for text in user_data]
            
            # Загружаем модель для создания эмбеддингов
            embed_model = resolve_embed_model(DEFAULT_EMBED_MODEL)
            # embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
            
            # Создаем индекс на основе документов
            index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
            
            print(f"Индекс для пользователя {user_id} успешно создан.")
            return index
            
    except Exception as e:
        print(f"Произошла ошибка при создании индекса: {e}")
        return None

# Пример использования (для тестирования) потом его удалю или закомментировать
async def main():
    # Создать индекс для пользователя с ID 1
    # Этот вызов вы будете использовать в вашем хендлере
    index = await create_and_save_index(user_id=1)
    if index:
        # Теперь вы можете использовать этот индекс для запросов
        query_engine = index.as_query_engine()
        response = await query_engine.query("Расскажи, что я знаю о уроках")
        print(response)

# Запускаем, если скрипт запущен напрямую
if __name__ == "__main__":
    asyncio.run(main())