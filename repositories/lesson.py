# repositories/lesson.py
from .base import BaseRepository
from database.models import Lesson 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

class LessonRepository(BaseRepository[Lesson]):
    def __init__(self, session: AsyncSession):
        super().__init__(Lesson, session)

    async def get_user_lessons(self, user_id: int, limit: int = 10, offset: int = 0) -> List[Lesson]:
        """Получает уроки конкретного пользователя."""
        stmt = select(self.model).where(self.model.user_id == user_id).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    