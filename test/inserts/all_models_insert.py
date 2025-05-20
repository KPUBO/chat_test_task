from sqlalchemy.ext.asyncio import AsyncSession

from test.inserts.chats_insert import chats_insert
from test.inserts.groups_insert import groups_insert
from test.inserts.message_read_statuses_insert import message_read_statuses_insert
from test.inserts.messages_insert import messages_insert
from test.inserts.users_groups_insert import users_groups_insert
from test.inserts.users_insert import users_insert


async def all_models_insert(session: AsyncSession) -> None:
    await users_insert(session)

    await groups_insert(session)

    await users_groups_insert(session)

    await chats_insert(session)

    await messages_insert(session)

    await message_read_statuses_insert(session)
