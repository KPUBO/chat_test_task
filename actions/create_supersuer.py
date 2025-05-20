import asyncio
import contextlib
import os

from api.dependencies.authentication.user_manager import get_user_manager
from api.dependencies.authentication.users import get_user_db
from core.models import db_helper
from core.authentication.user_manager import UserManager
from core.models.user_models.user import User
from core.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(db_helper.session_getter)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

default_email = os.getenv("DEFAULT_EMAIL", "admin@admin.com")
default_password = os.getenv("DEFAULT_PASSWORD", "admin")
default_name = 'admin'
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(user_manager: UserManager, user_create: UserCreate) -> User:
    user = await user_manager.create(user_create=user_create, safe=False)
    return user


async def create_superuser(
    email: str = default_email,
    password: str = default_password,
    name: str = default_name,
    is_active: str = default_is_active,
    is_superuser: str = default_is_superuser,
    is_verified: str = default_is_verified
):
    user_create = UserCreate(
        email=email,
        password=password,
        name=name,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_user(user_manager, user_create)


if __name__ == "__main__":
    asyncio.run(create_superuser())
