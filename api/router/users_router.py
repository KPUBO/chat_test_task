from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.service.users_service import UserService
from core.models import db_helper
from core.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('', response_model=List[UserRead])
async def read_users(
        session: AsyncSession = Depends(db_helper.session_getter)
):
    service = UserService(session)
    users = await service.get_all()
    return users


@router.get('/{user_id}')
async def read_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    service = UserService(session)
    user = await service.get_by_id(user_id)
    return user


@router.post('', response_model=UserCreate)
async def add_user(
        user: UserCreate,
        session: AsyncSession = Depends(db_helper.session_getter),

):
    service = UserService(session)
    user = service.insert_item(user=user)
    return await user


@router.put('/{user_id}', response_model=UserCreate)
async def update_user(
        user_id: int,
        user: UserCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    service = UserService(session)
    user = service.update_item(user_id=user_id, user=user)
    return await user


@router.delete('/{user_id}', response_model=UserCreate)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    service = UserService(session)
    user = await service.delete_item(user_id=user_id)
    return user
