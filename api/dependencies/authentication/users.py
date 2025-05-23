from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models.user_models.user import User


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield User.get_db(session=session)