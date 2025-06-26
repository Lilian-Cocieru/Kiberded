# """Implementation of the user table"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime
from datetime import datetime
from database.engine import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Внутренний ID
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)   # Telegram ID
    username: Mapped[str] = mapped_column(String, nullable=True)           # Username (если есть)
    language_code: Mapped[str] = mapped_column(String, default="ru")       # Язык
    model_name: Mapped[str] = mapped_column(String, default="qwen/qwen3-30b-a3b:free")  # Выбранная модель
    token_limit: Mapped[int] = mapped_column(Integer, default=100_000)     # Лимит бесплатных токенов
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)           # Сколько использовано бесплатно
    tokens_paid_used: Mapped[int] = mapped_column(Integer, default=0)      # Платные токены (через OpenRouter)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)       # Есть ли подписка
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Когда зарегистрировался
    lessons = relationship("Lesson", back_populates="user", cascade="all, delete-orphan")





# """Implementation of the user table"""
# from sqlalchemy import String, Integer, BigInteger, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from datetime import datetime
# from database.engine import Base
# from models.ai_model import AIModel

# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
#     username: Mapped[str | None] = mapped_column(String(32), nullable=True)
#     full_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
#     language_code: Mapped[str | None] = mapped_column(String(10), default='ru')  # By default, Russian but implementation will be the choice of language by the user
#     is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
#     subscription_active: Mapped[bool] = mapped_column(Boolean, default=False)
#     token_limit: Mapped[int] = mapped_column(Integer, default=100_000)  # For example, 100k tokens
#     ai_level: Mapped[str] = mapped_column(String(20), default='basic')  # можно связать с enum в будущем
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

#     ai_model_id: Mapped[int | None] = mapped_column(ForeignKey("ai_models.id"))
#     ai_model: Mapped["AIModel"] = relationship(backref="users")
