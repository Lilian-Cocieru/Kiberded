# repositories/voice_message.py
from .base import BaseRepository
from database.models import VoiceMessage
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class VoiceMessageRepository(BaseRepository[VoiceMessage]):
    def __init__(self, session: AsyncSession):
        super().__init__(VoiceMessage, session)

    async def get_by_file_id(self, file_id: str) -> Optional[VoiceMessage]:
        """Получает голосовое сообщение по Telegram file_id."""
        return await self.get_by_field("file_id", file_id)