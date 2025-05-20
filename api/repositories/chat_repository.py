from datetime import datetime
from typing import Sequence, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, join
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.repositories.base_repository import T
from core.connection_manager import manager
from core.models import Chat, Group, users_groups, Message, MessageReadStatus, User
from core.models import db_helper
from core.schemas.chat import ChatCreate
from core.schemas.message import MessageCreate


class ChatRepository:

    def __init__(self,
                 session: AsyncSession = Depends(db_helper.session_getter)):
        self.session = session
        self.model = Chat

    async def get_chat_by_id(self, chat_id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == chat_id)
        )
        chat = result.scalar()
        return chat

    async def get_all_chats(self,
                            offset: int,
                            limit: int) -> Optional[Sequence[T]]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        chats = result.scalars().all()
        if len(chats) == 0:
            raise HTTPException(status_code=404, detail="No chats found")

        return chats

    async def get_chats_by_group_id(self, group_id: int) -> Optional[Sequence[T]]:
        result = await self.session.execute(select(self.model).filter(self.model.group_id == group_id))
        chats = result.scalars().all()
        if len(chats) == 0:
            raise HTTPException(status_code=404, detail=f"No chats with {group_id} found")
        return chats

    async def get_chats_by_user_id(self, user_id: int) -> Optional[Sequence[T]]:
        stmt = (
            select(Group)
            .join(users_groups, Group.id == users_groups.c.group_id)
            .where(users_groups.c.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        groups = result.scalars().all()
        chats = []
        for group in groups:
            result = await self.session.execute(select(Chat).filter(Chat.group_id == group.id))
            chat = result.scalars().all()
            chats.append(chat)
        return chats

    async def create_chat(self, chat: ChatCreate) -> T:
        try:
            chat = Chat(**chat.model_dump())
            self.session.add(chat)
            await self.session.commit()
            return chat
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23503':
                raise HTTPException(status_code=404, detail=f"Group with {chat.group_id} not found")
            raise

    async def update_chat(self, chat: ChatCreate, chat_id: int, current_user: User) -> Optional[T]:
        chat_to_update = await self.session.get(Chat, chat_id)
        stmt = await self.session.execute(select(Group).where(Group.id == chat.group_id))
        group = stmt.scalar_one_or_none()
        if group.creator_id == current_user.id:
            update_data_dict = chat.model_dump()
            for k, v in update_data_dict.items():
                setattr(chat_to_update, k, v)
            await self.session.commit()
            return chat_to_update
        else:
            raise HTTPException(status_code=403, detail=f"You have no permissions to delete chat {chat_id}")

    async def delete_chat_by_id(self, chat_id, current_user: User) -> Optional[T]:
        chat = await self.session.get(Chat, chat_id)
        stmt = await self.session.execute(select(Group).where(Group.id == chat.group_id))
        group = stmt.scalar_one_or_none()
        if chat:
            if group.creator_id == current_user.id:
                await self.session.delete(chat)
                await self.session.commit()
                return chat
            else:
                raise HTTPException(status_code=403, detail=f"You have no permissions to delete chat {chat_id}")
        else:
            raise HTTPException(status_code=404, detail=f"Chat with {chat_id} not found")

    async def send_message_to_chat(self, chat_id: int, message: Message):
        stmt = (
            select(Chat)
            .options(joinedload(Chat.group))
            .filter(Chat.id == chat_id)
        )

        result = await self.session.execute(stmt)
        chat = result.scalar_one_or_none()

        if chat and chat.group:
            users_stmt = (
                select(users_groups.c.user_id)
                .select_from(
                    join(users_groups, Group, users_groups.c.group_id == Group.id)
                )
                .where(Group.id == chat.group.id)
            )
            users_result = await self.session.execute(users_stmt)
            users_ids = users_result.scalars().all()

        for user in users_ids:
            if message.sender_id != user:
                stmt = insert(MessageReadStatus).values(
                    message_id=message.id,
                    recipient_id=user,
                    is_read=False,
                    read_at=None,
                )
                await self.session.execute(stmt)
        await self.session.commit()

        await manager.broadcast(message, users_ids)


