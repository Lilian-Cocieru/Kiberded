

# from sqlalchemy import String, Integer
# from sqlalchemy.orm import Mapped, mapped_column
# from database.engine import Base

# class AIModel(Base):
#     __tablename__ = "ai_models"

#     id: Mapped[int] = mapped_column(primary_key=True)  # Уникальный ID модели в таблице
#     name: Mapped[str] = mapped_column(String(32), unique=True)  # Название модели — например "openai-gpt4", "yandex-giga"
#     level: Mapped[str] = mapped_column(String(16))  # Уровень модели — "basic", "pro", "ultra" (для определения доступа)
#     token_limit: Mapped[int] = mapped_column(Integer)  # Лимит токенов на использование этой модели
#     speed_rank: Mapped[int] = mapped_column(Integer)  # Условная скорость модели: чем меньше число — тем быстрее
#     description: Mapped[str] = mapped_column(String(128))  # Краткое описание — может использоваться в интерфейсе выбора






from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from database.engine import Base

class AIModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True) # Уникальный ID модели в таблице
    name: Mapped[str] = mapped_column(String, unique=True)  # Например: "Qwen 3"
    provider: Mapped[str] = mapped_column(String)           # Например: "OpenRouter"
    model_code: Mapped[str] = mapped_column(String, unique=True)  # Например: "qwen/qwen3-30b-a3b:free"
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False) # Платная ли модель
    default_limit: Mapped[int] = mapped_column(Integer, default=100_000)  # Лимит по умолчанию
