from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.chat_repository import ChatRepository
from api.services.base_service import T
from core.models import Chat, Message, User
from core.models import db_helper
from core.schemas.chat import ChatCreate


class ChatService:
    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: ChatRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        return await self.repository.get_chat_by_id(chat_id)

    async def get_all_chats(self,
                            offset: int,
                            limit: int) -> Optional[Sequence[Chat]]:
        return await self.repository.get_all_chats(offset=offset, limit=limit)

    async def get_chats_by_group_id(self, group_id: int) -> Optional[Sequence[Chat]]:
        return await self.repository.get_chats_by_group_id(group_id)

    async def get_chats_by_user_id(self, user_id: int) -> Optional[Sequence[Chat]]:
        return await self.repository.get_chats_by_user_id(user_id)

    async def create_chat(self, chat: ChatCreate) -> Chat:
        return await self.repository.create_chat(chat)

    async def update_chat(self, chat: ChatCreate, chat_id: int, current_user: User) -> Optional[Chat]:
        return await self.repository.update_chat(chat, chat_id, current_user)

    async def delete_chat_by_id(self, chat_id, current_user: User) -> Optional[T]:
        return await self.repository.delete_chat_by_id(chat_id, current_user)

    async def send_message_to_chat(self, chat_id: int, message: Message) -> Optional[T]:
        return await self.repository.send_message_to_chat(chat_id, message)
