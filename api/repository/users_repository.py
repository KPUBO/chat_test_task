from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import add

from core.models.user_models.user import User
from core.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_id(self, user_id) -> User:
        result = await self.session.execute(
            select(User).filter(User.id == user_id)
        )
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail=f"User by id={user_id} not found")
        return user

    async def get_all_users(self) -> Sequence[User]:
        result = await self.session.execute(
            select(User).order_by(User.id)
        )
        return result.scalars().all()

    async def create_user(self, user: UserCreate) -> User:
        user = User(**user.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, user: UserCreate):
        user_to_update = await self.session.get(User, user_id)
        if user_to_update is not None:
            update_data_dict = user.model_dump()
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            await self.session.commit()
            return user_to_update
        else:
            return None

    async def delete_user(self, user_id):
        user_to_delete = await self.session.get(User, user_id)
        if user_to_delete is not None:
            await self.session.delete(user_to_delete)
            await self.session.commit()
            return user_to_delete
        else:
            return None
