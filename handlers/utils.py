
# C:\Users\Computer\Desktop\python\Kiberded\handlers\utils.py
import asyncio
from aiogram.types import Message

TELEGRAM_TEXT_LIMIT = 4096

async def send_long_message(message: Message, text: str):
  """
  Разбивает длинный текст на части и отправляет их последовательно.
  """
  # Если текст короткий, отправляем сразу
  if len(text) <= TELEGRAM_TEXT_LIMIT:
    await message.answer(text, parse_mode='MarkdownV2')
    return
  # Если текст длинный, разбиваем его на куски
  chunks = [text[i:i + TELEGRAM_TEXT_LIMIT] for i in range(0, len(text), TELEGRAM_TEXT_LIMIT)]
  for chunk in chunks:
    await message.answer(chunk, parse_mode='MarkdownV2')
    # Небольшая задержка, чтобы избежать лимитов Telegram
    await asyncio.sleep(0.5)



# # C:\Users\Computer\Desktop\python\Kiberded\handlers\utils.py

# import asyncio
# from aiogram.types import Message
# import re

# TELEGRAM_TEXT_LIMIT = 4096

# async def send_long_message(message: Message, text: str):
#     """
#     Разбивает длинный текст на части и отправляет их последовательно.
#     С функцией экранирования если есть таблицы.
#     """
#     # Функция для экранирования символов
#     def escape_markdown(text):
#         # Используем регулярное выражение для замены
#         # Заменяем только символы вне блоков моноширинного кода
#         # Это более сложная логика, но для простоты можно просто заменить все
#         return re.sub(r'([_*[\]()~`>#+\-=|{}.!])', r'\\\1', text)

#     # Экранируем текст перед отправкой
#     escaped_text = escape_markdown(text)

#     # Добавляем параметр parse_mode для корректного отображения Markdown
#     # Проверяем, если длина текста меньше лимита, отправляем сразу
#     if len(escaped_text) <= TELEGRAM_TEXT_LIMIT:
#         await message.answer(escaped_text, parse_mode='MarkdownV2')
#         return
#     # Если текст длинный, разбиваем его на куски по 4096 символов
#     chunks = [escaped_text[i:i + TELEGRAM_TEXT_LIMIT] for i in range(0, len(escaped_text), TELEGRAM_TEXT_LIMIT)]

#     for chunk in chunks:
#         # Отправляем каждую часть с правильным форматированием
#         await message.answer(chunk, parse_mode='MarkdownV2')
#         # Опционально: небольшая задержка, чтобы избежать лимитов Telegram
#         await asyncio.sleep(0.5)
        