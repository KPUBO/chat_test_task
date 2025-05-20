from typing import Type

from fastapi import Depends, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


def get_entity_by_id(model: Type, param_name: str):
    async def dependency(
            entity_id: int = Path(..., alias=param_name),
            session: AsyncSession = Depends(db_helper.session_getter)
    ):
        result = await session.execute(select(model).where(model.id == entity_id))
        entity = result.scalar_one_or_none()
        if not entity:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return entity

    return dependency
