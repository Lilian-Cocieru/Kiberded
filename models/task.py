

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, Text, Boolean, DateTime
from datetime import datetime
from database.engine import Base

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








# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import Integer, ForeignKey, String, Text, Boolean, DateTime
# from datetime import datetime
# from database.engine import Base



    
# class Task(Base):
#     __tablename__ = "tasks"  # Название таблицы в БД

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   # Уникальный идентификатор задачи, автоинкремент
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))            # Внешний ключ на таблицу users — кому принадлежит задача
#     subject: Mapped[str] = mapped_column(String(100))                       # Название предмета, например: "математика", "физика"
#     lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))        # Внешний ключ на таблицы к уроку
#     description: Mapped[str] = mapped_column(Text)                          # Подробное описание задания (вопрос, задача и т.п.)
#     answer: Mapped[str] = mapped_column(Text, nullable=True)                # Ответ на задание (может быть пустым, если ещё не решено)
#     ai_checked: Mapped[bool] = mapped_column(Boolean, default=False)        # Было ли задание проверено ИИ (True/False)
#     grade: Mapped[int] = mapped_column(Integer, nullable=True)              # Оценка за выполнение (может быть None, если ещё не выставлена)
#     created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)   # Дата и время создания задания (устанавливается автоматически)
#     lesson = relationship("Lesson", back_populates="tasks", lazy="joined")  # Обратная связь к занятию



# class Task(Base):
#     __tablename__ = "tasks"

#     id: Mapped[int] = mapped_column(primary_key=True)


#     question: Mapped[str] = mapped_column(Text)                   # Задание/вопрос
#     correct_answer: Mapped[str] = mapped_column(Text)             # Правильный ответ
#     user_answer: Mapped[str] = mapped_column(Text, nullable=True) # Ответ пользователя
#     is_correct: Mapped[bool] = mapped_column(Boolean, default=False)  # Верно ли

#     created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

