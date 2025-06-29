


# C:\Users\Computer\Desktop\python\Kiberded\handlers\start.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from database.engine import SessionLocal
from repositories.user import UserRepository
from repositories.ai_model import AIModelRepository

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    async with SessionLocal() as session:
        user_repo = UserRepository(session)
        ai_model_repo = AIModelRepository(session)

        # Добавил full_name в вызов create_or_get_user
        user = await user_repo.create_or_get_user(
            tg_id=message.from_user.id,  # type: ignore
            username=message.from_user.username,  # type: ignore
            full_name=message.from_user.full_name # type: ignore
        )

        if user.ai_model_id is None:
            all_models = await ai_model_repo.get_all()
            if not all_models:
                await message.answer("Извините, сейчас нет доступных AI-моделей. Попробуйте позже.")
                return

            keyboard_buttons = []
            for model_obj in all_models:
                keyboard_buttons.append([types.InlineKeyboardButton(text=model_obj.name, callback_data=f"select_model:{model_obj.id}")])
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            await message.answer(
                f"Привет, {user.full_name or user.username}! Добро пожаловать! Пожалуйста, выберите AI-модель для работы:",
                reply_markup=keyboard
            )

        else:
            selected_model = await ai_model_repo.get_by_id(user.ai_model_id)  # type: ignore
            if selected_model:
                await message.answer(f"С возвращением, {user.full_name or user.username}! Ваша текущая модель: **{selected_model.name}**. Отправьте мне запрос!")
            else:
                await message.answer("Ваша предыдущая AI-модель не найдена. Пожалуйста, выберите новую.")
                all_models = await ai_model_repo.get_all()
                if all_models:
                    keyboard_buttons = []
                    for model_obj in all_models:
                        keyboard_buttons.append([types.InlineKeyboardButton(text=model_obj.name, callback_data=f"select_model:{model_obj.id}")])
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
                    await message.answer("Пожалуйста, выберите AI-модель:", reply_markup=keyboard)




# from aiogram import Router
# from aiogram.filters import CommandStart
# from aiogram.types import Message

# user_router = Router()

# @user_router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Добро пожаловать! Напишите свой запрос.')