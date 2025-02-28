import asyncio
import os

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.models import Base, db_helper
from main import main_app

pytestmark = pytest.mark.asyncio(loop_scope="session")

async_engine = create_async_engine(
    url=os.getenv('APP_CONFIG__TEST_DB__TEST_DATABASE_URL'),
    echo=False,
)


@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE {table.name} CASCADE;'))
            await session.commit()


@pytest.fixture(scope='session')
async def async_client(async_db) -> AsyncClient:
    async def override_get_db():
        try:
            yield async_db
        finally:
            await async_db.close()

    main_app.dependency_overrides[db_helper.session_getter] = override_get_db
    return AsyncClient(transport=ASGITransport(app=main_app), base_url='http://localhost')


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()