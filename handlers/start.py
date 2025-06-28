

# Пример использования в handlers/start.py или handlers/gen_handlers.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from database.engine import SessionLocal # Импортируем SessionLocal
from repositories.user import UserRepository
from repositories.ai_model import AIModelRepository
# ... другие импорты репозиториев

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    async with SessionLocal() as session: # Получаем асинхронную сессию
        user_repo = UserRepository(session)
        ai_model_repo = AIModelRepository(session) # Если нужна AI модель

        # Создаем или получаем пользователя
        # Поскольку ai_model_id теперь nullable, при создании он будет None,
        # пока пользователь не выберет модель.
        user = await user_repo.create_or_get_user(
            tg_id=message.from_user.id,  # type: ignore
            username=message.from_user.username  # type: ignore
        )

        # Пример: если пользователь ещё не выбрал модель, предложите ему
        if user.ai_model_id is None:
            # Здесь можем запросить AIModelRepository
            # и отправить инлайн-клавиатуру с выбором моделей.
            models = await ai_model_repo.get_all() # Получить все доступные модели
            model_names = [m.name for m in models]
            await message.answer(
                f"Привет, {user.username}! Добро пожаловать. Пожалуйста, выберите AI модель для работы:\n" +
                ", ".join(model_names) # Здесь будет логика инлайн-клавиатуры
            )
        else:
            # Если модель уже выбрана, приветствуем
            await message.answer(f"С возвращением, {user.username}! Ваша текущая модель: {user.ai_model.name}")  # type: ignore
        
        # Пример: создание урока
        # lesson_repo = LessonRepository(session)
        # new_lesson = await lesson_repo.create(user_id=user.id, title="Первое занятие")
        # await message.answer(f"Создано новое занятие: {new_lesson.title}")




# from aiogram import Router
# from aiogram.filters import CommandStart
# from aiogram.types import Message

# user_router = Router()

# @user_router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Добро пожаловать! Напишите свой запрос.')