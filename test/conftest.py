import asyncio
import os

from redis import asyncio as aioredis

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.models import Base, db_helper
from main import main_app
from test.inserts.all_models_insert import all_models_insert

REDIS_HOST = os.getenv('APP_CONFIG__REDIS_DB__HOST', 'localhost')
REDIS_PORT = os.getenv('APP_CONFIG__REDIS_DB__PORT', 6379)

pytestmark = pytest.mark.asyncio(loop_scope="session")

async_engine = create_async_engine(
    url=os.getenv('APP_CONFIG__TEST_DB__URL'),
    echo=False,
)


@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(
                text(f'TRUNCATE {table.name} RESTART IDENTITY CASCADE')
            )

        await all_models_insert(session)

        yield session
        await session.commit()

        await session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE {table.name} CASCADE;'))
            await session.commit()


@pytest.fixture(scope='function')
async def async_client(async_db) -> AsyncClient:
    async def override_get_db():
        try:
            yield async_db
        finally:
            await async_db.close()

    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
    FastAPICache.init(RedisBackend(redis), prefix="test-cache")
    yield AsyncClient(transport=ASGITransport(app=main_app), base_url='http://localhost')
    await FastAPICache.clear()


@pytest.fixture(scope='function')
async def get_user_token(async_client):
    async def _get_user_token(creds):
        login_response = await async_client.post("/api/auth/jwt/login", data={
            "username": f"{creds}@{creds}.com",
            "password": f"{creds}"
        })
        token = login_response.json()["access_token"]
        return token

    return _get_user_token


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
