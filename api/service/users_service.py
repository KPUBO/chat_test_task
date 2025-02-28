from typing import List, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from api.repository.users_repository import UserRepository
from core.models import User
from core.schemas.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(session)

    async def get_all_users(self) -> Sequence[User]:
        return await self.repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.repository.get_user_by_id(user_id)

    async def create_user(self, user: UserCreate) -> User:
        user = await self.repository.create_user(user)
        return user

    async def update_user(self, user_id: int, user: UserCreate):
        user = await self.repository.update_user(user_id, user)
        return user

    async def delete_user(self, user_id: int):
        user = await self.repository.delete_user(user_id)
        return user
