import jwt
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketState
from starlette.websockets import WebSocketDisconnect

from api.dependencies.deps_utils.utils import SECRET_KEY, get_ws_token, ChatAccessService
from api.dependencies.entity_finder import get_entity_by_id
from api.logger import logger
from api.services.chat_service import ChatService
from api.services.group_service import GroupService
from api.services.message_service import MessageService
from api.websocket.handlers import handle_history, handle_receiving_json, handle_create_chat
from api.websocket.websocket_entry_info import INFO
from core.connection_manager import manager
from core.models import User, Chat, db_helper

router = APIRouter()


def verify_jwt_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], audience=[
        "fastapi-users:auth"
    ])
    return payload


async def get_token_from_header(websocket: WebSocket):
    headers = dict(websocket.scope["headers"])

    if b"authorization" not in headers:
        await websocket.close(code=1008)
        return None

    auth_header = headers[b"authorization"].decode("utf-8")
    if not auth_header.startswith("Bearer "):
        await websocket.close(code=1008)
        return None

    return auth_header[7:]


async def check_user_access_to_chat(websocket: WebSocket,
                                    session: AsyncSession,
                                    chat_id: int,
                                    current_user: User, ):
    access_service = ChatAccessService(session)
    if not await access_service.check_access(chat_id=chat_id, user_id=current_user.id):
        await websocket.close(code=1008, reason="Access denied")
        return


@router.websocket("/info")
async def websocket_endpoint(websocket: WebSocket, ):
    await websocket.accept()
    await websocket.send_text(INFO)


@router.websocket("/create_chat")
async def create_chat(websocket: WebSocket,
                      current_user: User = Depends(get_ws_token),
                      chat_service: ChatService = Depends(),
                      group_service: GroupService = Depends(),
                      ):
    token = await get_token_from_header(websocket)
    if not token:
        return
    if verify_jwt_token(token):
        await manager.connect(user_id=current_user.id, websocket=websocket)
        try:
            while True:
                data = await websocket.receive_json()
                await handle_create_chat(
                    websocket=websocket,
                    chat_service=chat_service, group_service=group_service,
                    users_ids=data['data'],
                    chat_name=data['chat_name'],
                    current_user=current_user,
                )

        except WebSocketDisconnect:
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await manager.disconnect(current_user.id)
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
        finally:
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await manager.disconnect(current_user.id)


@router.websocket("/ws/chat/{chat_id}")
async def chat_entry_endpoint(websocket: WebSocket,
                              chat_id: int,
                              message_service: MessageService = Depends(),
                              chat_service: ChatService = Depends(),
                              group_service: GroupService = Depends(),
                              session: AsyncSession = Depends(db_helper.session_getter),
                              existing_chat=Depends(get_entity_by_id(Chat, 'chat_id')),
                              current_user: User = Depends(get_ws_token),
                              ):
    token = await get_token_from_header(websocket)
    if not token:
        return
    if verify_jwt_token(token):
        await check_user_access_to_chat(
            websocket=websocket,
            session=session,
            chat_id=chat_id,
            current_user=current_user,
        )
        await manager.connect(user_id=current_user.id, websocket=websocket)
        await handle_history(websocket=websocket, message_service=message_service, chat_id=chat_id)
        try:
            while True:
                data = await websocket.receive_json()
                await handle_receiving_json(websocket, data,
                                            chat_id=chat_id,
                                            chat_service=chat_service,
                                            message_service=message_service,
                                            current_user=current_user,
                                            group_service=group_service,
                                            )

        except WebSocketDisconnect:
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await manager.disconnect(current_user.id)
        except Exception as e:
            await websocket.send_json(
                {
                    "error": f'{e}',
                    "details": f"Неожиданная ошибка: {e}, переподключитесь к веб-сокету"
                }
            )
            logger.error(f"Неожиданная ошибка: {e}, переподключитесь к веб-сокету")
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await manager.disconnect(current_user.id)
        # finally:
        #     if websocket.client_state != WebSocketState.DISCONNECTED:
        #         await manager.disconnect(current_user.id)
