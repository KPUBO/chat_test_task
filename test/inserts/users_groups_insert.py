from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, users_groups


async def query_execution(session: AsyncSession, user_id: int, group_id: int):
    query = insert(users_groups).values(
        user_id=user_id,
        group_id=group_id
    )
    await session.execute(query)

users_groups_connection = [
    {
        'group_id': 1,
        'user_id': 1
    },
    {
        'group_id': 1,
        'user_id': 2
    },
    {
        'group_id': 2,
        'user_id': 3
    },
    {
        'group_id': 2,
        'user_id': 4
    },
    {
        'group_id': 2,
        'user_id': 5
    },
]


async def users_groups_insert(session: AsyncSession):
    for conn in users_groups_connection:
        await query_execution(session,
                              conn['user_id'],
                              conn['group_id'])
    await session.commit()
