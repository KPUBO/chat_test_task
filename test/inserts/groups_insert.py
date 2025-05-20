from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Group

groups = [
    {
        'name': 'TestGroup1',
        'creator_id': 1
    },
    {
        'name': 'TestGroup2',
        'creator_id': 3
    },

]


async def groups_insert(session: AsyncSession):
    group_models = [Group(**group) for group in groups]
    session.add_all(group_models)
    await session.commit()
