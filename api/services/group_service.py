from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.group_repository import GroupRepository
from api.services.base_service import T
from core.models import Group, User
from core.models import db_helper
from core.schemas.group import GroupCreate


class GroupService:
    def __init__(
            self,
            session: AsyncSession = Depends(db_helper.session_getter),
            repo: GroupRepository = Depends()
    ):
        self.session = session
        self.repository = repo

    async def get_group_by_id(self, group_id: int) -> Optional[Group]:
        return await self.repository.get_group_by_id(group_id)

    async def get_all_groups(self,
                             offset: int,
                             limit: int) -> Optional[Sequence[Group]]:
        return await self.repository.get_all_groups(offset=offset, limit=limit)

    async def create_group(self, group: GroupCreate) -> Group:
        return await self.repository.create_group(group)

    async def add_user_to_group(self, group_id: int, user_id: int, current_user: User) -> User:
        return await self.repository.add_user_to_group(group_id, user_id, current_user)

    async def update_group(self, group: GroupCreate, group_id: int, current_user: User) -> Optional[Group]:
        return await self.repository.update_group(group, group_id, current_user)

    async def delete_group_by_id(self, group_id, current_user: User) -> Optional[T]:
        return await self.repository.delete_group_by_id(group_id, current_user=current_user)

    async def delete_user_from_group(self, group_id: int, user_id: int, current_user: User) -> Optional[T]:
        return await self.repository.delete_user_from_group(group_id, user_id, current_user)
