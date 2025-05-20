from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from api.dependencies.authentication.users import get_user_db
from core.authentication.user_manager import UserManager


async def get_user_manager(
    users_db: Annotated["SQLAlchemyUserDatabase", Depends(get_user_db)]
):
    yield UserManager(users_db)
