

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from datetime import datetime
from database.engine import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    title: Mapped[str] = mapped_column(String(256))           # Название занятия или темы
    summary: Mapped[str] = mapped_column(Text, nullable=True) # Краткий итог/резюме
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("User", back_populates="lessons", lazy="joined")  # Связь обратно к пользователю
    tasks = relationship("Task", back_populates="lesson", cascade="all, delete-orphan")
