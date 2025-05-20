from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models.access_token import AccessToken


async def get_access_token_db(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    yield AccessToken.get_db(session=session)