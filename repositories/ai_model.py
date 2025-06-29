# C:\Users\Computer\Desktop\python\Kiberded\repositories\ai_model.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

from database.models import AIModel 
from repositories.base import BaseRepository 

class AIModelRepository(BaseRepository[AIModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=AIModel, session=session) 

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[AIModel]: # Этот метод нужен для show_models_keyboard
        result = await self.session.execute(select(self.model).limit(limit).offset(offset))
        return list(result.scalars().all())

    # Если вам нужен метод get_all_active, оставьте его.
    # async def get_all_active(self) -> list[AIModel]:
    #     result = await self.session.execute(select(self.model).where(self.model.is_active == True))
    #     return list(result.scalars().all())


# # repositories/ai_model.py
# from .base import BaseRepository
# from database.models import AIModel 
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Optional

# class AIModelRepository(BaseRepository[AIModel]):
#     def __init__(self, session: AsyncSession):
#         super().__init__(AIModel, session)

#     # Добавим специфические методы для AIModel, если нужны будут в будуещем
#     async def get_by_model_code(self, model_code: str) -> Optional[AIModel]:
#         return await self.get_by_field("model_code", model_code)
    