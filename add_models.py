

# C:\Users\Computer\Desktop\python\Kiberded\add_models.py
import asyncio
from database.engine import SessionLocal, engine
from database.models import Base, AIModel
from sqlalchemy import select # Не забудьте импортировать select

async def add_default_ai_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        existing_models = await session.execute(
            select(AIModel)
        )
        existing_model_names = {model.name for model in existing_models.scalars().all()}

        models_to_add = []
        
        # ДОБАВЬТЕ ЗНАЧЕНИЕ ДЛЯ 'provider'
        if "Google Gemini 2.5 Flash" not in existing_model_names:
            models_to_add.append(AIModel(name="Google Gemini 2.5 Flash", provider="Google", model_code="google/gemini-1.5-flash"))
        
        if "Qwen 30B" not in existing_model_names:
            models_to_add.append(AIModel(name="Qwen 30B", provider="Alibaba", model_code="qwen/qwen3-30b-a3b:free"))
            
        if "Mixtral 8x7B" not in existing_model_names:
            models_to_add.append(AIModel(name="Mixtral 8x7B", provider="Mistral AI", model_code="mistralai/mixtral-8x7b-instruct:free"))
        
        # Продолжите добавлять другие модели с указанием провайдера

        if models_to_add:
            session.add_all(models_to_add)
            await session.commit()
            print(f"Добавлено {len(models_to_add)} новых AI-моделей в базу данных.")
        else:
            print("Все основные AI-модели уже существуют в базе данных.")

if __name__ == "__main__":
    print("Запуск скрипта для добавления AI-моделей...")
    asyncio.run(add_default_ai_models())
    print("Скрипт завершен.")






# # C:\Users\Computer\Desktop\python\Kiberded\add_models.py
# import asyncio
# from sqlalchemy import select
# from database.engine import SessionLocal, engine
# from database.models import Base, AIModel

# async def add_default_ai_models():
#     async with engine.begin() as conn:
#         # Создаем все таблицы, если их еще нет.
#         # Если таблицы уже существуют и схема не менялась, это безопасно.
#         await conn.run_sync(Base.metadata.create_all)

#     async with SessionLocal() as session:
#         # Проверяем, существуют ли уже модели, чтобы избежать дублирования
#         existing_models = await session.execute(
#             select(AIModel)
#         )
#         existing_model_names = {model.name for model in existing_models.scalars().all()}

#         models_to_add = []
#         if "Google Gemini 2.5 Flash" not in existing_model_names:
#             models_to_add.append(AIModel(name="Google Gemini 2.5 Flash", model_code="google/gemini-1.5-flash")) # Используем актуальное имя
#         if "Qwen 30B" not in existing_model_names:
#             models_to_add.append(AIModel(name="Qwen 30B", model_code="qwen/qwen3-30b-a3b:free"))
#         if "Mixtral 8x7B" not in existing_model_names:
#             models_to_add.append(AIModel(name="Mixtral 8x7B", model_code="mistralai/mixtral-8x7b-instruct:free"))
#         # Можете добавить другие модели, которые поддерживает OpenRouter
#         # model_code должны соответствовать тому, что указано на сайте OpenRouter.ai

#         if models_to_add:
#             session.add_all(models_to_add)
#             await session.commit()
#             print(f"Добавлено {len(models_to_add)} новых AI-моделей в базу данных.")
#         else:
#             print("Все основные AI-модели уже существуют в базе данных.")

# if __name__ == "__main__":
#     print("Запуск скрипта для добавления AI-моделей...")
#     asyncio.run(add_default_ai_models())
#     print("Скрипт завершен.")