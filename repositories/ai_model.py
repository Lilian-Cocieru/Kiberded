# repositories/ai_model.py
from .base import BaseRepository
from database.models import AIModel 
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class AIModelRepository(BaseRepository[AIModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(AIModel, session)

    # Добавим специфические методы для AIModel, если нужны будут в будуещем
    async def get_by_model_code(self, model_code: str) -> Optional[AIModel]:
        return await self.get_by_field("model_code", model_code)
    