# repositories/task.py
from .base import BaseRepository
from database.models import Task # Убедитесь, что это правильный импорт
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_lesson_tasks(self, lesson_id: int, limit: int = 100, offset: int = 0) -> List[Task]:
        """Получает задачи для конкретного урока."""
        stmt = select(self.model).where(self.model.lesson_id == lesson_id).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    