from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, DateTime, Boolean
from datetime import datetime
from database.engine import Base

class VoiceMessage(Base):
    __tablename__ = "voice_messages"  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   # Уникальный ID голосового сообщения
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))            # Внешний ключ: кто отправил сообщение
    file_id: Mapped[str] = mapped_column(String(255))                        # Telegram file_id для загрузки аудио
    transcribed_text: Mapped[str] = mapped_column(String(2048), nullable=True)  # Расшифрованный текст, если был
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)      # Было ли сообщение обработано
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)   # Дата и время загрузки голосового

    user = relationship("User", back_populates="voice_messages", lazy="joined")  # Связь с пользователем
