














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

    # --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
    async def create_or_get_user(self, tg_id: int, username: Optional[str] = None, full_name: Optional[str] = None) -> User:
        """Создает пользователя, если его нет, или возвращает существующего."""
        user = await self.get_by_tg_id(tg_id)
        if user is None:
            # Передаём full_name при создании
            user = await self.create(tg_id=tg_id, username=username, full_name=full_name) 
        else:
            # Обновляем username или full_name, если они изменились или были None
            needs_update = False
            update_data = {}
            if username and user.username != username:
                update_data['username'] = username
                needs_update = True
            if full_name and user.full_name != full_name: # type: ignore Предполагается, что у User есть поле full_name
                update_data['full_name'] = full_name
                needs_update = True
            
            if needs_update:
                user = await self.update(user.id, **update_data)
        
        if user is None: # На всякий случай, хотя create уже должен вернуть User
            raise ValueError(f"User with tg_id={tg_id} could not be created or retrieved.")
        return user
    # --- КОНЕЦ ИЗМЕНЕНИЙ ---


# # repositories/user.py
# from .base import BaseRepository
# from database.models import User 
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Optional

# class UserRepository(BaseRepository[User]):
#     def __init__(self, session: AsyncSession):
#         super().__init__(User, session)

#     async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
#         """Получает пользователя по Telegram ID."""
#         return await self.get_by_field("tg_id", tg_id)

#     async def create_or_get_user(self, tg_id: int, username: Optional[str] = None) -> User:
#         """Создает пользователя, если его нет, или возвращает существующего."""
#         user = await self.get_by_tg_id(tg_id)
#         if user is None:
#             user = await self.create(tg_id=tg_id, username=username)
#         else:
#             # Можно обновить username, если он изменился или был None
#             if username and user.username != username:
#                 user = await self.update(user.id, username=username)
#         if user is None:
#             raise ValueError(f"User with tg_id={tg_id} could not be created or retrieved.")
#         return user
    