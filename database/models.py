from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import Text, DateTime, ForeignKey
from datetime import datetime
from database.engine import Base



class AIModel(Base):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True) # Уникальный ID модели в таблице
    name: Mapped[str] = mapped_column(String, unique=True)  # Например: "Qwen 3"
    provider: Mapped[str] = mapped_column(String)           # Например: "OpenRouter"
    model_code: Mapped[str] = mapped_column(String, unique=True)  # Например: "qwen/qwen3-30b-a3b:free"
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False) # Платная ли модель
    default_limit: Mapped[int] = mapped_column(Integer, default=100_000)  # Лимит по умолчанию


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    title: Mapped[str] = mapped_column(String(256))           # Название занятия или темы
    summary: Mapped[str] = mapped_column(Text, nullable=True) # Краткий итог/резюме
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("User", back_populates="lessons", lazy="joined")  # Связь обратно к пользователю
    tasks = relationship("Task", back_populates="lesson", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"  # Название таблицы в БД

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Уникальный ID задачи
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))           # Ссылка на пользователя
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))       # Ссылка на урок
    subject: Mapped[str] = mapped_column(String(100))                      # Название предмета
    description: Mapped[str] = mapped_column(Text)                         # Содержание задания
    answer: Mapped[str] = mapped_column(Text, nullable=True)              # Ответ, если есть
    ai_checked: Mapped[bool] = mapped_column(Boolean, default=False)      # Проверено ли ИИ
    grade: Mapped[int] = mapped_column(Integer, nullable=True)            # Оценка, если есть
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Дата создания

    lesson = relationship("Lesson", back_populates="tasks", lazy="joined")  # Обратная связь к уроку


class VoiceMessage(Base):
    __tablename__ = "voice_messages"  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   # Уникальный ID голосового сообщения
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))            # Внешний ключ: кто отправил сообщение
    file_id: Mapped[str] = mapped_column(String(255))                        # Telegram file_id для загрузки аудио
    transcribed_text: Mapped[str] = mapped_column(String(2048), nullable=True)  # Расшифрованный текст, если был
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)      # Было ли сообщение обработано
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)   # Дата и время загрузки голосового

    user = relationship("User", back_populates="voice_messages", lazy="joined")  # Связь с пользователем

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


class Payment(Base):
    pass