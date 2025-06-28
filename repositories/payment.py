# repositories/payment.py
from .base import BaseRepository
from database.models import Payment
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Payment, session)

    async def get_user_payments(self, user_id: int, limit: int = 10, offset: int = 0) -> List[Payment]:
        """Получает платежи конкретного пользователя."""
        stmt = select(self.model).where(self.model.user_id == user_id).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_payment_system_id(self, ps_id: str) -> Optional[Payment]:
        """Получает платеж по ID платежной системы."""
        return await self.get_by_field("payment_system_id", ps_id)
    