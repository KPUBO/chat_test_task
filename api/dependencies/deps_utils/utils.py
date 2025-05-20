import json
import logging
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from redis import asyncio as aioredis
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.websockets import WebSocket

from core.config import settings
from core.models import User, Chat, users_groups, Group
from core.models import db_helper
from core.schemas.user import UserRead

REDIS_HOST = os.getenv('APP_CONFIG__REDIS_DB__HOST', 'localhost')
REDIS_PORT = os.getenv('APP_CONFIG__REDIS_DB__PORT', 6379)

SECRET_KEY = settings.access_token.verification_token_secret
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/jwt/login")
redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/0")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="fastapi-users:auth")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        logging.info(f'{e}')
        raise credentials_exception

    cached_user = await redis.get(f"user:{user_id}")
    if cached_user:
        return User(**json.loads(cached_user))

    user = await session.execute(
        select(User).filter(User.id == int(user_id))
    )
    user = user.scalars().first()

    if user is None:
        raise credentials_exception

    if user:
        user_cache = UserRead.model_validate(user)
        await redis.setex(f"user:{user_id}", 3600, user_cache.model_dump_json())
    return user


async def get_token_from_header(websocket: WebSocket):
    # Извлекаем заголовки из подключения WebSocket
    headers = dict(websocket.scope["headers"])

    # Проверяем наличие заголовка Authorization
    if b"authorization" not in headers:
        await websocket.close(code=1008)  # 1008 = Policy Violation
        return None

    # Получаем токен (формат: "Bearer <token>")
    auth_header = headers[b"authorization"].decode("utf-8")
    if not auth_header.startswith("Bearer "):
        await websocket.close(code=1008)
        return None

    return auth_header[7:]  # Возвращаем токен (без "Bearer ")


async def get_ws_token(
        websocket: WebSocket,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = await get_token_from_header(websocket)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="fastapi-users:auth")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        logging.info(f'{e}')
        raise credentials_exception

    cached_user = await redis.get(f"user:{user_id}")
    if cached_user:
        return User(**json.loads(cached_user))

    user = await session.execute(
        select(User).filter(User.id == int(user_id))
    )
    user = user.scalars().first()

    if user is None:
        raise credentials_exception

    if user:
        user_cache = UserRead.model_validate(user)
        await redis.setex(f"user:{user_id}", 3600, user_cache.model_dump_json())
    return user


def check_superuser(current_user: User = Depends(get_current_user)):
    if current_user.is_superuser != True:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


class ChatAccessService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_access(self, chat_id: int, user_id: int) -> bool:
        stmt = (
            select(exists().where(
                (Chat.id == chat_id) &
                (users_groups.c.user_id == user_id) &
                (Group.id == Chat.group_id) &
                (Group.id == users_groups.c.group_id)
            ))
        )
        result = await self.session.execute(stmt)
        return result.scalar()
