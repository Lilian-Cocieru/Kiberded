# C:\Users\Computer\Desktop\python\Kiberded\services\ai_models_sync.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import ALL_MODELS
from database.models import AIModel
from database.engine import SessionLocal



async def sync_ai_models():
    """Синхронизируем модели из config.py с таблицей ai_models"""
    async with SessionLocal() as session:
        async with session.begin():
            for model_data in ALL_MODELS:
                stmt = select(AIModel).where(AIModel.name == model_data["name"])
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if not model:
                    # Добавляем модель в базу, если её нет
                    new_model = AIModel(
                        id=model_data.get("id"),
                        name=model_data["name"],
                        provider=model_data.get("provider"),
                        model_code=model_data.get("model_code"),
                        is_paid=model_data.get("is_paid", False),
                        default_limit=model_data.get("default_limit", 100_000),
                        is_active=model_data.get("is_active", True),
                    )
                    session.add(new_model)
        await session.commit()
