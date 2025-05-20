import logging
import os
import platform
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Dict, Callable, Awaitable, Any

import redis as aioredis
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.websockets import WebSocket

from api.auth import router as auth_router
from api.logger import logger
from api.routers import router
from api.routers.websocket_router import router as websocket_router
from core.config import settings
from core.models.db_helper import db_helper


REDIS_HOST = os.getenv('APP_CONFIG__REDIS_DB__HOST', 'localhost')
REDIS_PORT = os.getenv('APP_CONFIG__REDIS_DB__PORT', 6379)



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")
    logger = logging.getLogger("uvicorn")
    current_os = platform.system()
    if current_os == "Windows":
        logger.info(f"Documentation: http://{settings.run.host}:{settings.run.port}/docs")
    if current_os == "Linux":
        logger.info(f"Documentation: http://{settings.run.host}:8001/docs")

    yield

    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.include_router(router,
                        prefix=settings.api.prefix)
main_app.include_router(auth_router,
                        prefix=settings.api.prefix)
main_app.include_router(websocket_router)

if __name__ == '__main__':
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
