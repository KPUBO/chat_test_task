from datetime import datetime
from typing import Sequence, Optional

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.base_repository import BaseRepository, T
from core.models import db_helper
from core.models.user_models.user import User
from core.schemas.user import UserCreate


class UserRepository:

    def __init__(self,
                 session: AsyncSession = Depends(db_helper.session_getter)):
        self.session = session
        self.model = User

    async def get_all(self) -> Sequence[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, item_id) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter(self.model.id == item_id)
        )
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail=f"User by id={item_id} not found")
        return user

    async def insert_item(self, user: UserCreate) -> T:
        user = User(**user.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_item(self, user_id: int, user: UserCreate) -> Optional[T]:
        user_to_update = await self.session.get(User, user_id)
        if user_to_update is not None:
            update_data_dict = user.model_dump()
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            user_to_update.updated_at = datetime.utcnow()
            await self.session.commit()
            return user_to_update
        else:
            return None

    async def delete_by_id(self, user_id) -> Optional[T]:
        user_to_delete = await self.session.get(User, user_id)
        if user_to_delete is not None:
            await self.session.delete(user_to_delete)
            await self.session.commit()
            return user_to_delete
        else:
            return None
