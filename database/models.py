
# C:\Users\Computer\Desktop\python\Kiberded\database\models.py

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer, String, Boolean, Text, DateTime, ForeignKey, Numeric 
from datetime import datetime
from typing import Optional

# --- Вспомогательная функция для UTC времени ---
# Это поможет убедиться, что default и onupdate используют один и тот же часовой пояс
def current_utc_datetime():
    return datetime.utcnow()


class Base(DeclarativeBase, AsyncAttrs):
    pass


class AIModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True) # Уникальный ID модели в таблице
    name: Mapped[str] = mapped_column(String, unique=True) # Например: "Qwen 3"
    provider: Mapped[str] = mapped_column(String)         # Например: "OpenRouter"
    model_code: Mapped[str] = mapped_column(String, unique=True) # Например: "qwen/qwen3-30b-a3b:free"
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False) # Платная ли модель
    default_limit: Mapped[int] = mapped_column(Integer, default=100_000) # Лимит по умолчанию
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) # Новое поле: активна ли модель


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    title: Mapped[str] = mapped_column(String(256))       # Название занятия или темы
    summary: Mapped[str] = mapped_column(Text, nullable=True) # Краткий итог/резюме
    created_at: Mapped[datetime] = mapped_column(default=current_utc_datetime)
    updated_at: Mapped[datetime] = mapped_column(default=current_utc_datetime, onupdate=current_utc_datetime) # Новое поле: дата последнего обновления

    user = relationship("User", back_populates="lessons", lazy="joined")  # Связь обратно к пользователю
    tasks = relationship("Task", back_populates="lesson", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"  # Название таблицы в БД

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # Уникальный ID задачи
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))         # Ссылка на пользователя
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))      # Ссылка на урок
    subject: Mapped[str] = mapped_column(String(100))                     # Название предмета
    description: Mapped[str] = mapped_column(Text)                        # Содержание задания
    answer: Mapped[str] = mapped_column(Text, nullable=True)              # Ответ, если есть
    ai_checked: Mapped[bool] = mapped_column(Boolean, default=False)      # Проверено ли ИИ
    grade: Mapped[int] = mapped_column(Integer, nullable=True)            # Оценка, если есть
    created_at: Mapped[datetime] = mapped_column(DateTime, default=current_utc_datetime) # Дата создания
    updated_at: Mapped[datetime] = mapped_column(default=current_utc_datetime, onupdate=current_utc_datetime) # Новое поле: дата последнего обновления

    lesson = relationship("Lesson", back_populates="tasks", lazy="joined") # Обратная связь к уроку


class VoiceMessage(Base):
    __tablename__ = "voice_messages"  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # Уникальный ID голосового сообщения
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))          # Внешний ключ: кто отправил сообщение
    file_id: Mapped[str] = mapped_column(String(255))                     # Telegram file_id для загрузки аудио
    transcribed_text: Mapped[str] = mapped_column(String(2048), nullable=True) # Расшифрованный текст, если был
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)    # Было ли сообщение обработано
    created_at: Mapped[datetime] = mapped_column(default=current_utc_datetime) # Дата и время загрузки голосового

    user = relationship("User", back_populates="voice_messages", lazy="joined") # Связь с пользователем


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str] = mapped_column(String, default="ru")     # Язык
    ai_model_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ai_models.id"), nullable=True)     # Ссылка на AIModel.id ИЗМЕНЕНО: теперь nullable=True, без default
    ai_model: Mapped[Optional["AIModel"]] = relationship("AIModel")      # Связь с объектом AIModel relationship тоже Optional
    token_limit: Mapped[int] = mapped_column(Integer, default=100_000)   # Лимит бесплатных токенов
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)         # Сколько использовано бесплатно
    tokens_paid_used: Mapped[int] = mapped_column(Integer, default=0)    # Платные токены (через OpenRouter)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)     # Есть ли подписка
    created_at: Mapped[datetime] = mapped_column(DateTime, default=current_utc_datetime) # Когда зарегистрировался
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=current_utc_datetime, onupdate=current_utc_datetime) # Дата последней активности

    lessons = relationship("Lesson", back_populates="user", cascade="all, delete-orphan")
    voice_messages = relationship("VoiceMessage", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan") # Новое отношение для Payment


class Payment(Base):
    __tablename__ = "payments" # Множественное число, как и у других таблиц

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) # Кто сделал платеж
    
    # Детали платежа
    amount: Mapped[float] = mapped_column(Numeric(10, 2)) # Сумма (10 цифр, 2 после запятой для валюты)
    currency: Mapped[str] = mapped_column(String(10)) # Валюта (e.g., 'RUB', 'USD')
    
    # Статус и идентификаторы
    status: Mapped[str] = mapped_column(String(50), default="pending") # Статус платежа ('pending', 'completed', 'failed', 'refunded')
    payment_system_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True) # ID транзакции в платежной системе
    
    # Цель платежа
    description: Mapped[str] = mapped_column(Text, nullable=True) # Описание: "Покупка токенов", "Премиум-подписка"
    payment_type: Mapped[str] = mapped_column(String(50)) # Тип платежа (e.g., 'token_pack', 'premium_subscription')
    
    # Влияние на токены (если применимо)
    tokens_added: Mapped[int] = mapped_column(Integer, nullable=True) # Сколько токенов было добавлено пользователю
    
    # Даты
    created_at: Mapped[datetime] = mapped_column(DateTime, default=current_utc_datetime) # Время создания записи о платеже
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True) # Время завершения/подтверждения платежа
    
    # Связь с пользователем
    user = relationship("User", back_populates="payments", lazy="joined")
    