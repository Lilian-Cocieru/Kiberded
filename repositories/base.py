# repositories/base.py
from typing import TypeVar, Type, Generic, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase

# Определяем TypeVar для типа модели, чтобы можно было использовать дженерики
ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, **kwargs) -> ModelType:
        """Создает новую запись в базе данных."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except IntegrityError:
            await self.session.rollback()
            raise # Перевыбрасываем исключение для обработки выше (например, UNIQUE constraint failed)

    async def get(self, id: int) -> Optional[ModelType]:
        """Получает запись по ID."""
        return await self.session.get(self.model, id)

    async def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        """Получает запись по значению любого поля."""
        stmt = select(self.model).where(getattr(self.model, field_name) == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Получает все записи."""
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Обновляет запись по ID."""
        stmt = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model)  # type: ignore
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance:
            await self.session.commit()
            await self.session.refresh(instance)
        return instance

    async def delete(self, id: int) -> bool:
        """Удаляет запись по ID."""
        stmt = delete(self.model).where(self.model.id == id)  # type: ignore
        result = await self.session.execute(stmt)
        if result.rowcount > 0:
            await self.session.commit()
            return True
        await self.session.rollback()
        return False
    