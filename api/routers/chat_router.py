from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.deps_utils.utils import get_current_user
from api.dependencies.entity_finder import get_entity_by_id
from api.services.chat_service import ChatService
from core.models import Chat, User, Group
from core.schemas.chat import ChatRead, ChatCreate

router = APIRouter(
    prefix="/chats",
    tags=["Chat"],
)


@router.get("",
            response_model=List[ChatRead],
            dependencies=[Depends(get_current_user)],
            summary="Get all chats", )
async def get_all_chats(
        limit: int = 10,
        offset: int = 0,
        service: ChatService = Depends()
):
    chats = await service.get_all_chats(offset=offset, limit=limit)
    return chats


@router.get('/{chat_id}',
            dependencies=[Depends(get_entity_by_id(Chat, 'chat_id'))],
            summary='Get chat by it\'s id')
async def read_chat_by_id(
        chat_id: int,
        service: ChatService = Depends()

):
    chat = await service.get_chat_by_id(chat_id)
    return chat

@router.get('/get_chat_by_group_id/{group_id}',
            dependencies=[Depends(get_entity_by_id(Group, 'group_id'))],
            summary='Get chat by id group of users')
async def get_chat_by_group_id(
        group_id: int,
        service: ChatService = Depends()
):
    return await service.get_chats_by_group_id(group_id)


@router.post('',
             response_model=ChatRead,
             summary='Add chat to database')
async def add_chat(
        chat: ChatCreate,
        service: ChatService = Depends()
):
    chat = service.create_chat(chat=chat)
    return await chat


@router.put('/{chat_id}',
            dependencies=[Depends(get_entity_by_id(Chat, 'chat_id'))],
            response_model=ChatRead,
            summary='Update chat by it\'s id')
async def update_chat(
        chat_id: int,
        chat: ChatCreate,
        service: ChatService = Depends(),
        current_user: User = Depends(get_current_user)
):
    chat = service.update_chat(chat_id=chat_id, chat=chat, current_user=current_user)
    return await chat


@router.delete('/{chat_id}',
               dependencies=[Depends(get_entity_by_id(Chat, 'chat_id'))],
               response_model=ChatRead,
               summary='Get chat by it\'s id')
async def delete_chat(
        chat_id: int,
        service: ChatService = Depends(),
        current_user: User = Depends(get_current_user)
):
    chat = await service.delete_chat_by_id(chat_id=chat_id, current_user=current_user)
    return chat
