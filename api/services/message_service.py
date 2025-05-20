from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.message_repository import MessageRepository
from api.services.base_service import T
from core.models import Message, User
from core.models import db_helper
from core.schemas.message import MessageCreate


class MessageService:
    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: MessageRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return await self.repository.get_message_by_id(message_id)

    async def get_all_messages(self,
                               offset: int,
                               limit: int) -> Optional[Sequence[Message]]:
        return await self.repository.get_all_messages(offset=offset, limit=limit)

    async def get_all_messages_by_chat_id(self, chat_id: int) -> Sequence[Message]:
        return await self.repository.get_all_messages_by_chat_id(chat_id)

    async def create_message(self, message: MessageCreate, current_user: User) -> Message:
        return await self.repository.create_message(message=message, current_user=current_user)

    async def update_message(self, message: MessageCreate, message_id: int, current_user: User) -> Optional[Message]:
        return await self.repository.update_message(message, message_id, current_user)

    async def delete_message_by_id(self, message_id, current_user: User) -> Optional[T]:
        return await self.repository.delete_message_by_id(message_id, current_user)

    async def load_message_history_to_chat(self, chat_id: int):
        return await self.repository.load_message_history_to_chat(chat_id)

    async def mark_message_as_read(self, message_id: int, user_id: int):
        return await self.repository.mark_message_as_read(message_id, user_id)
