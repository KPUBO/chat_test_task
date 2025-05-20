from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message

messages = [
    {
        'chat_id': 1,
        'sender_id': 1,
        'content': 'Test content for chat 1 from user 1',
        'is_fully_read': False
    },
    {
        'chat_id': 1,
        'sender_id': 2,
        'content': 'Test content for chat 1 from user 2',
        'is_fully_read': False
    },
    {
        'chat_id': 2,
        'sender_id': 3,
        'content': 'Test content for chat 2 from user 3',
        'is_fully_read': False
    },
    {
        'chat_id': 2,
        'sender_id': 4,
        'content': 'Test content for chat 2 from user 4',
        'is_fully_read': False
    },
    {
        'chat_id': 2,
        'sender_id': 5,
        'content': 'Test content for chat 2 from user 5',
        'is_fully_read': False
    },
]


async def messages_insert(session: AsyncSession):
    message_models = [Message(**message) for message in messages]
    session.add_all(message_models)
    await session.commit()
