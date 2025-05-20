from datetime import datetime
from typing import Optional, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import T
from core.models import Group, users_groups, Chat, User
from core.models import db_helper
from core.models.chat_models.chat import TypeChat
from core.schemas.group import GroupCreate


class GroupRepository:

    def __init__(self,
                 session: AsyncSession = Depends(db_helper.session_getter)):
        self.session = session
        self.model = Group

    async def get_group_by_id(self, group_id: int) -> Optional[Group]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == group_id)
        )
        group = result.scalar_one()
        return group

    async def get_all_groups(self,
                             offset: int,
                             limit: int) -> Optional[Sequence[Group]]:
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        groups = result.scalars().all()
        if len(groups) == 0:
            raise HTTPException(status_code=404, detail="No groups found")
        return groups

    async def get_groups_by_user_id(self, user_id: int) -> Optional[Sequence[Group]]:
        stmt = select(users_groups).where(users_groups.c.user_id == user_id)
        result = await self.session.execute(stmt)
        groups = result.scalars().all()
        if len(groups) == 0:
            raise HTTPException(status_code=404, detail="No groups found")
        return groups

    async def create_group(self, group: GroupCreate) -> Group:
        group = Group(**group.model_dump())
        self.session.add(group)
        await self.session.commit()
        return group

    async def add_user_to_group(self, group_id: int, user_id: int, current_user: User):
        try:
            stmt = insert(users_groups).values(user_id=user_id, group_id=group_id)
            await self.session.execute(stmt)

            stmt = select(Chat).filter(Chat.group_id == group_id)
            result = await self.session.execute(stmt)
            chat = result.scalars().first()

            stmt = select(Group).filter(Group.id == chat.group_id)
            group_result = await self.session.execute(stmt)
            group = group_result.scalar_one_or_none()

            if group.creator_id == current_user.id:

                stmt = select(users_groups.c.user_id).filter(users_groups.c.group_id == group.id)
                users_result = await self.session.execute(stmt)
                users = users_result.scalars().all()
                if len(users) >= 2 and chat.type != TypeChat.grouped:
                    setattr(chat, 'type', 'grouped')
                await self.session.commit()
                return f'User {user_id} added successfully'
            else:
                raise HTTPException(status_code=403, detail="Only group owners can add users to chat")
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="User already exists in this group")

    async def update_group(self, group: GroupCreate, group_id: int, current_user: User) -> Optional[Group]:
        group_to_update = await self.session.get(Group, group_id)
        if group_to_update.creator_id == current_user.id:
            update_data_dict = group.model_dump()
            for k, v in update_data_dict.items():
                setattr(group_to_update, k, v)
            group_to_update.updated_at = datetime.utcnow()
            await self.session.commit()
            return group_to_update
        else:
            raise HTTPException(status_code=403, detail="Only group owners can update group")

    async def delete_group_by_id(self, group_id, current_user: User) -> Optional[T]:
        group_to_delete = await self.session.get(Group, group_id)
        if group_to_delete.creator_id == current_user.id or current_user.is_superuser is True:
            await self.session.delete(group_to_delete)
            await self.session.commit()
            return group_to_delete
        else:
            raise HTTPException(status_code=403, detail="Only group owners can delete group")

    async def delete_user_from_group(self, group_id: int, user_id: int, current_user: User):
        try:
            group = await self.session.get(Group, group_id)
            if group.creator_id == current_user.id or user_id == current_user.id or current_user.is_superuser is True:
                stmt = await self.session.execute(
                    select(users_groups).where(users_groups.c.group_id == group_id,
                                               users_groups.c.user_id == user_id)
                )
                user_in_group = stmt.scalar_one_or_none()
                if user_in_group is None:
                    raise HTTPException(status_code=404, detail="User not found in this group")
                stmt = delete(users_groups).where(
                    (users_groups.c.user_id == user_id) &
                    (users_groups.c.group_id == group_id)
                )
                await self.session.execute(stmt)
                await self.session.commit()
                return 'User deleted from group successfully'
            else:
                raise HTTPException(status_code=403,
                                    detail="Only group owners and user himself can delete users from chat ")
        except IntegrityError as e:
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23505':
                raise HTTPException(status_code=409, detail="User already exists in this group")
            if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23503':
                raise HTTPException(status_code=409, detail="User not found in this group")
