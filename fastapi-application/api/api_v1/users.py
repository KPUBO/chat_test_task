from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_all_users, create_user
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
    users = await get_all_users(session=session)
    return users


@router.post('', response_model=UserCreate)
async def add_user(
        user: UserCreate,
        session: AsyncSession = Depends(db_helper.session_getter),

):
    user = create_user(session=session, user=user)
    return await user
