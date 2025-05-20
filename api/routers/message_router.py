from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.deps_utils.utils import get_current_user
from api.dependencies.entity_finder import get_entity_by_id
from api.services.message_service import MessageService
from core.models import Message, User, Chat
from core.schemas.message import MessageRead, MessageCreate

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("",
            response_model=List[MessageRead],
            summary="Get all messages", )
async def get_all_messages(
        limit: int = 10,
        offset: int = 0,
        service: MessageService = Depends()
):
    messages = await service.get_all_messages(offset=offset, limit=limit)
    return messages


@router.get('/{message_id}',
            dependencies=[Depends(get_entity_by_id(Message, 'message_id'))],
            summary='Get message by it\'s id')
async def get_message_by_id(
        message_id: int,
        service: MessageService = Depends()

):
    message = await service.get_message_by_id(message_id)
    return message


@router.get('/get_messages_by_chat_id/{chat_id}',
            dependencies=[Depends(get_entity_by_id(Chat, 'chat_id'))],
            summary='Get all messages by chat_id')
async def get_all_messages_by_chat_id(
        chat_id: int,
        service: MessageService = Depends()
):
    messages = await service.get_all_messages_by_chat_id(chat_id)
    return messages


@router.post('',
             response_model=MessageRead,
             summary='Add message to database')
async def add_message(
        message: MessageCreate,
        service: MessageService = Depends(),
        current_user: User = Depends(get_current_user),
):
    message = service.create_message(message=message, current_user=current_user)
    return await message


@router.put('/{message_id}',
            dependencies=[Depends(get_entity_by_id(Message, 'message_id'))],
            response_model=MessageRead,
            summary='Update message by it\'s id')
async def update_message(
        message_id: int,
        message: MessageCreate,
        service: MessageService = Depends(),
        current_user: User = Depends(get_current_user)
):
    message = service.update_message(message_id=message_id, message=message, current_user=current_user)
    return await message


@router.delete('/{message_id}',
               dependencies=[Depends(get_entity_by_id(Message, 'message_id'))],
               response_model=MessageRead,
               summary='Get message by it\'s id')
async def delete_message(
        message_id: int,
        service: MessageService = Depends(),
        current_user: User = Depends(get_current_user)
):
    message = await service.delete_message_by_id(message_id=message_id, current_user=current_user)
    return message


@router.patch('/read_message/{message_id}',
              dependencies=[Depends(get_entity_by_id(Message, 'message_id'))])
async def read_message(
        message_id: int,
        service: MessageService = Depends(),
        current_user: User = Depends(get_current_user),
):
    message = await service.mark_message_as_read(message_id=message_id, user_id=current_user.id)
    return message
