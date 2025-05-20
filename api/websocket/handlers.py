from typing import List

from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.services.chat_service import ChatService
from api.services.group_service import GroupService
from api.services.message_service import MessageService
from core.models import User
from core.models.chat_models.chat import TypeChat
from core.schemas.chat import ChatCreate
from core.schemas.group import GroupCreate
from core.schemas.message import MessageCreate


async def handle_history(websocket: WebSocket,
                         chat_id: int,
                         message_service: MessageService):
    message_history = await message_service.load_message_history_to_chat(chat_id)
    await websocket.send_json({
        "type": "history",
        "data": [jsonable_encoder(msg) for msg in message_history]
    })


async def handle_new_message(chat_id: int,
                             message,
                             message_service: MessageService,
                             chat_service: ChatService,
                             current_user: User,
                             ):
    data = MessageCreate(
        chat_id=chat_id,
        content=message,
    )
    sending_message = await message_service.create_message(message=data, current_user=current_user)

    await chat_service.send_message_to_chat(chat_id=chat_id, message=sending_message)


async def handle_read_messages(websocket: WebSocket,
                               message_id: int,
                               message_service: MessageService,
                               current_user: User):
    await message_service.mark_message_as_read(message_id=message_id, user_id=current_user.id)
    await websocket.send_json({
        "type": f"Message {message_id} is read",
    })


async def handle_get_all_chats_of_current_user_query(
        websocket: WebSocket,
        user_id: int,
        chat_service: ChatService
):
    chats = await chat_service.get_chats_by_user_id(user_id=user_id)
    if chats:

        await websocket.send_json(
            {
                "type": "chats",
                "data": [jsonable_encoder(chat) for chat in chats]
            }
        )
    else:
        await websocket.send_json(
            {
                "type": "error",
                'data': 'No chats found'
            }
        )


async def handle_add_user_to_chat(websocket: WebSocket,
                                  user_id: int,
                                  chat_id: int,
                                  chat_service: ChatService,
                                  group_service: GroupService,
                                  current_user: User, ):
    chat = await chat_service.get_chat_by_id(chat_id=chat_id)
    await group_service.add_user_to_group(group_id=chat.group_id, user_id=user_id, current_user=current_user)
    await websocket.send_json(
        {
            "type": "chats",
            'data': f'User {user_id} added to chat'
        }
    )


async def handle_delete_user_from_chat(websocket: WebSocket,
                                       user_id: int,
                                       chat_id: int,
                                       chat_service: ChatService,
                                       group_service: GroupService,
                                       current_user: User,
                                       ):
    chat = await chat_service.get_chat_by_id(chat_id=chat_id)
    await group_service.delete_user_from_group(group_id=chat.group_id, user_id=user_id, current_user=current_user)
    await websocket.send_json(
        {
            "type": "chats",
            'data': f'User {user_id} deleted from chat'
        }
    )


async def handle_create_chat(websocket: WebSocket,
                             chat_service: ChatService,
                             group_service: GroupService,
                             users_ids: List[int],
                             chat_name: str,
                             current_user: User, ):
    group = GroupCreate(name=chat_name,
                        creator_id=current_user.id, )
    group = await group_service.create_group(group)
    if len(users_ids) >= 2:
        type = TypeChat.grouped
    else:
        type = TypeChat.private
    chat = ChatCreate(
        name=chat_name,
        type=type,
        group_id=group.id
    )
    chat = await chat_service.create_chat(chat)
    await group_service.add_user_to_group(group.id, user_id=current_user.id, current_user=current_user)
    for user_id in users_ids:
        await group_service.add_user_to_group(group.id, user_id=user_id, current_user=current_user)

    await websocket.send_json(
        {
            "type": "chats",
            "data": "Chat created",
            'chat_id': chat.id
        }
    )


async def handle_delete_chat(websocket: WebSocket,
                             chat_id: int,
                             chat_service: ChatService,
                             current_user: User,
                             ):
    await chat_service.delete_chat_by_id(chat_id=chat_id, current_user=current_user)
    await websocket.send_json(
        {
            "type": "chats",
            "data": "Chat deleted"
        }
    )


async def handle_delete_message(message_id: int,
                                message_service: MessageService,
                                current_user: User, ):
    await message_service.delete_message_by_id(message_id=message_id, current_user=current_user)


async def handle_get_message_by_id(message_id: int, message_service: MessageService):
    return await message_service.get_message_by_id(message_id=message_id)


async def handle_receiving_json(websocket: WebSocket, data, **kwargs):
    if data['type'] == 'sending_message':
        await handle_new_message(chat_id=kwargs['chat_id'],
                                 message=data['data'],
                                 message_service=kwargs['message_service'],
                                 chat_service=kwargs['chat_service'],
                                 current_user=kwargs['current_user'], )

    if data['type'] == 'reading_messages':
        for message_id in data['data']:
            await handle_read_messages(websocket=websocket,
                                       message_id=message_id,
                                       message_service=kwargs['message_service'],
                                       current_user=kwargs['current_user'])

    if data['type'] == 'get_chats':
        await handle_get_all_chats_of_current_user_query(
            websocket=websocket,
            user_id=kwargs['current_user'].id,
            chat_service=kwargs['chat_service'])

    if data['type'] == 'add_user_to_chat':
        for user_id in data['data']:
            await handle_add_user_to_chat(
                websocket=websocket,
                user_id=user_id,
                chat_id=kwargs['chat_id'],
                chat_service=kwargs['chat_service'],
                group_service=kwargs['group_service'],
                current_user=kwargs['current_user'],
            )

    if data['type'] == 'delete_user_from_chat':
        for user_id in data['data']:
            await handle_delete_user_from_chat(
                websocket=websocket,
                user_id=user_id,
                chat_id=kwargs['chat_id'],
                chat_service=kwargs['chat_service'],
                group_service=kwargs['group_service'],
                current_user=kwargs['current_user'],
            )

    if data['type'] == 'delete_chat':
        await handle_delete_chat(
            websocket=websocket,
            chat_id=kwargs['chat_id'],
            chat_service=kwargs['chat_service'],
            current_user=kwargs['current_user']
        )
        raise WebSocketDisconnect

    if data['type'] == 'delete_messages':
        for message_id in data['data']:
            await handle_delete_message(
                message_id=message_id,
                message_service=kwargs['message_service'],
                current_user=kwargs['current_user']
            )
        await websocket.send_json(
            {
                "type": "messages",
                "data": f"Messages {data['data']} deleted"
            }
        )
