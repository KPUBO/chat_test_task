from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.deps_utils.utils import get_current_user

from api.services.users_service import UserService
from core.models import db_helper
from core.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('',
            response_model=List[UserRead],
            dependencies=[Depends(get_current_user)])
async def read_users(
        service: UserService = Depends()
):
    users = await service.get_all()
    return users


@router.get('/{user_id}')
async def read_user_by_id(
        user_id: int,
        service: UserService = Depends()
):
    user = await service.get_by_id(user_id)
    return user


