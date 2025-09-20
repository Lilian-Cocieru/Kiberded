
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
