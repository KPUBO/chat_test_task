from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.users_repository import UserRepository
from api.services.base_service import BaseService
from core.models import User, db_helper
from core.schemas.user import UserCreate


class UserService(BaseService):

    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: UserRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_all(self) -> Sequence[User]:
        return await self.repository.get_all()

    async def get_by_id(self, user_id: int) -> User:
        return await self.repository.get_by_id(user_id)

    async def insert_item(self, user: UserCreate) -> User:
        user = await self.repository.insert_item(user)
        return user

    async def update_item(self, user_id: int, user: UserCreate) -> Optional[User]:
        user = await self.repository.update_item(user_id, user)
        return user

    async def delete_item(self, user_id: int):
        user = await self.repository.delete_by_id(user_id)
        return user
