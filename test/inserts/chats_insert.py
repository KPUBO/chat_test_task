from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Chat
from core.models.chat_models.chat import TypeChat

chats = [
    {
        'name': 'TestChat1',
        'group_id': 1,
        "type": TypeChat.private,
    },
    {
        'name': 'TestChat2',
        'group_id': 2,
        "type": TypeChat.grouped,
    },
]

async def chats_insert(session: AsyncSession):
    chat_models = [Chat(**chat) for chat in chats]
    session.add_all(chat_models)
    await session.commit()