from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MessageReadStatus

message_read_statuses_connection = [
    {
        'message_id': 1,
        'recipient_id': 2,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 2,
        'recipient_id': 1,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 3,
        'recipient_id': 4,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 3,
        'recipient_id': 5,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 4,
        'recipient_id': 3,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 4,
        'recipient_id': 5,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 5,
        'recipient_id': 3,
        'is_read': False,
        'read_at': None
    },
    {
        'message_id': 5,
        'recipient_id': 4,
        'is_read': False,
        'read_at': None
    }
]


async def message_read_statuses_insert(session: AsyncSession):
    message_read_status_models = [MessageReadStatus(**message_read_status) for message_read_status in
                                  message_read_statuses_connection]
    session.add_all(message_read_status_models)
    await session.commit()
