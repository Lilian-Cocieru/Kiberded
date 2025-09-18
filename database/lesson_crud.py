# C:\Users\Computer\Desktop\python\Kiberded\database\lesson_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Lesson

async def add_lesson(
    session: AsyncSession,
    user_id: int,
    title: str,
    summary: str
):
    """
    Добавляет новый урок в базу данных.
    
    Args:
        session: Асинхронная сессия SQLAlchemy.
        user_id: ID пользователя из Telegram.
        title: Название урока.
        summary: Краткое описание или заметки по уроку.
    """
    new_lesson = Lesson(
        user_id=user_id,
        title=title,
        summary=summary
    )
    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)
    return new_lesson