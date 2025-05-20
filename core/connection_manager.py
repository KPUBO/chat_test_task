import asyncio
from typing import Dict, List

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from api.logger import logger
from core.models import db_helper, Message


class ConnectionManager:
    def __init__(self,
                 session: AsyncSession = Depends(db_helper.session_getter)):
        self.active_connections: Dict[int, WebSocket] = {}
        self.session = session
        self.lock = asyncio.Lock()
        self.handled_messages = set()

    async def connect(self, user_id: int, websocket: WebSocket):
        async with self.lock:
            await websocket.accept()
            self.active_connections[user_id] = websocket
            logger.info(f"Пользователь {user_id} подключился. Всего: {len(self.active_connections)}")

    async def disconnect(self, user_id: int):
        async with self.lock:
            if user_id in self.active_connections:
                del self.active_connections[user_id]
                logger.info(f"Пользователь {user_id} отключился. Осталось: {len(self.active_connections)}")

    async def send_personal_message(self, message: Message, user_id: int):
        if message.id in self.handled_messages:
            return
        self.handled_messages.add(message.id)
        async with self.lock:
            if user_id in self.active_connections:
                await self.active_connections[user_id].send_text(message.content)

    async def broadcast(self, message: Message, users: List[int]):
        if message.id in self.handled_messages:
            return
        self.handled_messages.add(message.id)
        for user_id in users:
            if user_id in self.active_connections:
                await self.active_connections[user_id].send_json(jsonable_encoder(message))


manager = ConnectionManager()
