# repositories/user.py
from .base import BaseRepository
from database.models import User # Убедитесь, что это правильный импорт
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
        """Получает пользователя по Telegram ID."""
        return await self.get_by_field("tg_id", tg_id)

    async def create_or_get_user(self, tg_id: int, username: Optional[str] = None) -> User:
        """Создает пользователя, если его нет, или возвращает существующего."""
        user = await self.get_by_tg_id(tg_id)
        if user is None:
            user = await self.create(tg_id=tg_id, username=username)
        else:
            # Можно обновить username, если он изменился или был None
            if username and user.username != username:
                user = await self.update(user.id, username=username)
        if user is None:
            raise ValueError(f"User with tg_id={tg_id} could not be created or retrieved.")
        return user
    