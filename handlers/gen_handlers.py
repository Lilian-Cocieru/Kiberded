

from aiogram import F, Router, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode # Добавляем импорт ParseMode
from aiogram.exceptions import TelegramAPIError # Добавляем импорт TelegramAPIError для обработки ошибок API

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from ai_utils import ai_generate
from database.engine import SessionLocal
from repositories.user import UserRepository
from repositories.ai_model import AIModelRepository

# --- Добавляем логирование ---
import logging
logger = logging.getLogger(__name__)

gen_router = Router() # Используем gen_router, чтобы соответствовать импорту в bot.py

class Gen(StatesGroup):
    waiting = State()

@gen_router.message(F.state == Gen.waiting)
async def stop_flood(message: Message):
    logger.info(f"Получено сообщение от пользователя {message.from_user.id} во время состояния 'waiting'.") # type: ignore
    await message.answer('Подождите, ваш запрос генерируется. Не отправляйте сообщения пока идет генерация.')

@gen_router.message()
async def generating(message: Message, state: FSMContext, bot: Bot):
    user_info = "Unknown"
    if message.from_user:
        user_info = f"{message.from_user.full_name or message.from_user.username}"
    logger.info(f"Хендлер 'generating' получил сообщение от пользователя {getattr(message.from_user, 'id', 'Unknown')} ({user_info}).")
    
    async with SessionLocal() as session:
        user_repo = UserRepository(session)
        ai_model_repo = AIModelRepository(session)

        if not message.from_user or not hasattr(message.from_user, "id"):
            logger.error("Ошибка: не удалось определить пользователя Telegram (отсутствует from_user или id).")
            await message.answer("Ошибка: не удалось определить пользователя Telegram. Пожалуйста, попробуйте снова.")
            return
        
        user = await user_repo.get_by_tg_id(message.from_user.id)
        if not user:
            logger.warning(f"Пользователь с TG ID {message.from_user.id} не найден в базе данных. Просим отправить /start.")
            await message.answer("Я вас не нашёл в базе данных. Пожалуйста, отправьте команду /start, чтобы начать.")
            return

        logger.info(f"Пользователь {user.tg_id} найден. Проверяем, выбрана ли AI-модель (AI Model ID: {user.ai_model_id}).")
        if user.ai_model_id is None:
            logger.info(f"Пользователь {user.tg_id} не имеет выбранной AI-модели. Запрашиваем список моделей.")
            all_models = await ai_model_repo.get_all() 
            if not all_models:
                logger.error("Нет доступных AI-моделей в базе данных (ai_models таблица пуста или все неактивны).")
                await message.answer("Извините, сейчас нет доступных AI-моделей. Попробуйте позже.")
                return

            logger.info(f"Найдено {len(all_models)} AI-моделей. Формируем клавиатуру.")
            keyboard_buttons = []
            for model_obj in all_models:
                keyboard_buttons.append([types.InlineKeyboardButton(text=model_obj.name, callback_data=f"select_model:{model_obj.id}")])
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            await message.answer("Пожалуйста, выберите AI-модель для начала работы:", reply_markup=keyboard)
            return

        logger.info(f"Пользователь {user.tg_id} имеет выбранную модель ({user.ai_model_id}). Устанавливаем состояние 'waiting'.")
        await state.set_state(Gen.waiting)
        try:
            # Используем .get() из BaseRepository
            selected_model = await ai_model_repo.get(user.ai_model_id) 
            if not selected_model:
                logger.warning(f"Выбранная AI-модель (ID: {user.ai_model_id}) для пользователя {user.tg_id} не найдена или неактивна.")
                await message.answer("Выбранная AI-модель временно недоступна. Пожалуйста, выберите другую модель.")
                await state.clear()
                return

            logger.info(f"Начинаем генерацию ответа для пользователя {user.tg_id} с моделью: {selected_model.model_code}.")
            response = await ai_generate(message.text, selected_model.model_code)
            await message.answer(response)
            logger.info(f"Ответ успешно сгенерирован и отправлен пользователю {user.tg_id}.")
        except Exception as e:
            logger.exception(f"Критическая ошибка при генерации ответа для пользователя {user.tg_id}:")
            await message.answer(f"Произошла ошибка при генерации ответа. Пожалуйста, попробуйте позже. Подробности: {e}")
        finally:
            await state.clear()
            logger.info(f"Состояние FSM для пользователя {user.tg_id} очищено после генерации.")

@gen_router.callback_query(F.callback_query.data.startswith("select_model:")) 
async def select_model_callback(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"CallbackQuery получен! Data: '{callback_query.data}' от пользователя TG ID: {callback_query.from_user.id}")

    if not callback_query.data:
        logger.error(f"CallbackQuery от пользователя {callback_query.from_user.id} не содержит данных.")
        await bot.send_message(callback_query.from_user.id, "Ошибка: не удалось получить данные выбора модели.")
        await callback_query.answer("Ошибка: не удалось получить данные выбора модели.", show_alert=True)
        return
    
    model_id = None
    try:
        model_id = int(callback_query.data.split(":")[1])
        logger.info(f"Извлечен model_id: {model_id} из CallbackQuery.")
    except (ValueError, IndexError) as e:
        logger.exception(f"Ошибка при парсинге model_id из CallbackQuery данных: '{callback_query.data}'. Ошибка: {e}")
        await callback_query.answer("Ошибка при обработке выбора модели. Неверный формат данных.", show_alert=True)
        return 

    async with SessionLocal() as session:
        user_repo = UserRepository(session)
        ai_model_repo = AIModelRepository(session) 

        user = await user_repo.get_by_tg_id(callback_query.from_user.id)
        if user:
            logger.info(f"Пользователь {user.tg_id} найден. Попытка обновить ai_model_id на {model_id}.")
            
            # --- Инициализируем updated_user здесь, перед try-блоком ---
            updated_user = None 

            try:
                updated_user = await user_repo.update(user.id, ai_model_id=model_id)
                
                if updated_user and updated_user.ai_model_id:
                    # Используем .get() из BaseRepository
                    selected_model = await ai_model_repo.get(updated_user.ai_model_id) 
                    message_text = "" 
                    if selected_model:
                        message_text = f"Вы выбрали модель: **{selected_model.name}**. Теперь можете отправить свой запрос!"
                        logger.info(f"Модель **{selected_model.name}** успешно установлена для пользователя {user.id}.")
                    else:
                        message_text = "Выбранная AI-модель временно недоступна. Пожалуйста, выберите другую модель."
                        logger.warning(f"Выбранная модель с ID {updated_user.ai_model_id} не найдена в БД после обновления пользователя.")

                    # --- Обработка редактирования сообщения с учетом InaccessibleMessage ---
                    if callback_query.message:
                        try:
                            # Проверяем, что сообщение доступно для редактирования
                            if isinstance(callback_query.message, Message): # Убедимся, что это объект Message
                                await callback_query.message.edit_text(message_text, parse_mode=ParseMode.MARKDOWN) 
                                logger.info(f"Сообщение для пользователя {user.id} отредактировано.")
                            else:
                                # Если это InaccessibleMessage или другой не-Message тип, отправляем новое сообщение
                                logger.warning(f"callback_query.message не является Message (тип: {type(callback_query.message)}). Отправляем новое сообщение.")
                                await bot.send_message(callback_query.from_user.id, message_text, parse_mode=ParseMode.MARKDOWN)

                        except TelegramAPIError as e: # Ловим ошибки API Telegram
                            logger.exception(f"Ошибка Telegram API при редактировании сообщения для пользователя {user.id}: {e.message}. Отправляем новое сообщение.")
                            await bot.send_message(callback_query.from_user.id, message_text, parse_mode=ParseMode.MARKDOWN)
                        except Exception as e: # Ловим другие общие ошибки
                            logger.exception(f"Неизвестная ошибка при редактировании сообщения для пользователя {user.id}: {e}. Отправляем новое сообщение.")
                            await bot.send_message(callback_query.from_user.id, message_text, parse_mode=ParseMode.MARKDOWN)
                    else:
                        logger.warning(f"callback_query.message отсутствует. Отправляем новое сообщение.")
                        await bot.send_message(callback_query.from_user.id, message_text, parse_mode=ParseMode.MARKDOWN)
                else:
                    error_message = "Не удалось установить выбранную модель."
                    logger.error(f"Не удалось обновить ai_model_id для пользователя {user.id}. 'updated_user' или 'updated_user.ai_model_id' - None.")
                    
                    # --- Обработка редактирования сообщения с учетом InaccessibleMessage ---
                    if callback_query.message:
                        try:
                            if isinstance(callback_query.message, Message):
                                await callback_query.message.edit_text(error_message) 
                            else:
                                logger.warning(f"callback_query.message не является Message (тип: {type(callback_query.message)}). Отправляем новое сообщение об ошибке.")
                                await bot.send_message(callback_query.from_user.id, error_message)
                        except TelegramAPIError as e:
                            logger.exception(f"Ошибка Telegram API при редактировании сообщения (ошибка обновления модели) для пользователя {user.id}: {e.message}. Отправляем новое сообщение.")
                            await bot.send_message(callback_query.from_user.id, error_message)
                        except Exception as e:
                            logger.exception(f"Неизвестная ошибка при редактировании сообщения (ошибка обновления модели) для пользователя {user.id}: {e}. Отправляем новое сообщение.")
                            await bot.send_message(callback_query.from_user.id, error_message)
                    else:
                        logger.warning(f"callback_query.message отсутствует. Отправляем новое сообщение об ошибке.")
                        await bot.send_message(callback_query.from_user.id, error_message)
            except Exception as e:
                logger.exception(f"Ошибка при обновлении пользователя {user.id} с ai_model_id={model_id}: {e}")
                await bot.send_message(callback_query.from_user.id, "Произошла ошибка при сохранении выбранной модели. Пожалуйста, попробуйте снова.")
        else:
            error_message = "Ошибка: Пользователь не найден. Пожалуйста, отправьте /start."
            logger.error(f"Пользователь не найден в БД при обработке callback_query (TG ID: {callback_query.from_user.id}).")
            
            # --- Обработка редактирования сообщения с учетом InaccessibleMessage ---
            if callback_query.message:
                try:
                    if isinstance(callback_query.message, Message):
                        await callback_query.message.edit_text(error_message) 
                    else:
                        logger.warning(f"callback_query.message не является Message (тип: {type(callback_query.message)}). Отправляем новое сообщение об ошибке пользователя.")
                        await bot.send_message(callback_query.from_user.id, error_message)
                except TelegramAPIError as e:
                    logger.exception(f"Ошибка Telegram API при редактировании сообщения (пользователь не найден) для пользователя {callback_query.from_user.id}: {e.message}. Отправляем новое сообщение.")
                    await bot.send_message(callback_query.from_user.id, error_message)
                except Exception as e:
                    logger.exception(f"Неизвестная ошибка при редактировании сообщения (пользователь не найден) для пользователя {callback_query.from_user.id}: {e}. Отправляем новое сообщение.")
                    await bot.send_message(callback_query.from_user.id, error_message)
            else:
                logger.warning(f"callback_query.message отсутствует. Отправляем новое сообщение об ошибке пользователя.")
                await bot.send_message(callback_query.from_user.id, error_message)

    await callback_query.answer() # Это убирает индикатор загрузки/часики с кнопки в Telegram
    await state.clear()
    logger.info(f"Обработка CallbackQuery для пользователя {callback_query.from_user.id} завершена, состояние FSM очищено.")







