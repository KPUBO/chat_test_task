from datetime import datetime
from typing import Optional, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import T
from core.models import Message, User, MessageReadStatus
from core.models import db_helper
from core.schemas.message import MessageCreate


class MessageRepository:

    def __init__(self,
                 session: AsyncSession = Depends(db_helper.session_getter)):
        self.session = session
        self.model = Message

    async def get_message_by_id(self, message_id: int) -> Optional[Message]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == message_id)
        )
        message = result.scalar()
        return message

    async def get_all_messages(self,
                               offset: int,
                               limit: int) -> Optional[Sequence[Message]]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        messages = result.scalars().all()
        if len(messages) == 0:
            raise HTTPException(status_code=404, detail="No messages found")
        return messages

    async def get_all_messages_by_chat_id(self, chat_id: int) -> Optional[Sequence[Message]]:
        result = await self.session.execute(select(self.model).
                                            where(self.model.chat_id == chat_id).
                                            order_by(self.model.timestamp.desc()))
        messages = result.scalars().all()
        return messages

    async def create_message(self, message: MessageCreate, current_user: User) -> Message:
        message = Message(**message.model_dump())
        message.sender_id = current_user.id
        self.session.add(message)
        await self.session.commit()
        return message

    async def update_message(self, message: MessageCreate, message_id: int, current_user: User) -> Optional[Message]:
        message_to_update = await self.session.get(Message, message_id)
        if message_to_update.sender_id == current_user.id:
            update_data_dict = message.model_dump()
            for k, v in update_data_dict.items():
                setattr(message_to_update, k, v)
            await self.session.commit()
            return message_to_update
        else:
            raise HTTPException(status_code=403, detail="Only sender can update message")

    async def delete_message_by_id(self, message_id, current_user: User) -> Optional[T]:
        message_to_delete = await self.session.get(Message, message_id)
        if message_to_delete.sender_id == current_user.id:
            await self.session.delete(message_to_delete)
            await self.session.commit()
            return message_to_delete
        else:
            raise HTTPException(status_code=403, detail="Only sender can delete message")

    async def load_message_history_to_chat(self, chat_id: int):
        messages = await self.get_all_messages_by_chat_id(chat_id)
        return messages

    async def mark_message_as_read(self, message_id: int, user_id: int):
        stmt = await self.session.execute(select(MessageReadStatus).filter(
            MessageReadStatus.message_id == message_id,
            MessageReadStatus.recipient_id == user_id
        ))
        message_status = stmt.scalar_one_or_none()
        if message_status:
            if not message_status.is_read:
                setattr(message_status, "is_read", True)
                setattr(message_status, "read_at", datetime.now())
                await self.session.commit()
        else:
            raise HTTPException(status_code=404, detail='Note not found')
        message_to_update = await self.session.get(Message, message_id)
        stmt = await self.session.execute(select(MessageReadStatus).filter(
            MessageReadStatus.message_id == message_id
        ))
        message_statuses = stmt.scalars().all()
        for message_status in message_statuses:
            if not message_status.is_read:
                break
        else:
            setattr(message_to_update, "is_fully_read", True)
            await self.session.commit()
        return message_to_update

