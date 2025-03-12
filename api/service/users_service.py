from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.repository.users_repository import UserRepository
from api.service.base_service import BaseService
from core.models import User
from core.schemas.user import UserCreate


class UserService(BaseService):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(User, session)

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
