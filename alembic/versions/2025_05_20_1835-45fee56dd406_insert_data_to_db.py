"""Insert data to db

Revision ID: 45fee56dd406
Revises: 48aea12a7a7f
Create Date: 2025-05-20 18:35:25.505270

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from passlib.context import CryptContext

from core.models.chat_models.chat import TypeChat

# revision identifiers, used by Alembic.
revision: str = "45fee56dd406"
down_revision: Union[str, None] = "48aea12a7a7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    op.execute("""
            SELECT setval('chats_id_seq', COALESCE((SELECT MAX(id) FROM chats), 1), false)
        """)
    op.execute("""
                SELECT setval('groups_id_seq', COALESCE((SELECT MAX(id) FROM groups), 1), false)
            """)
    op.execute("""
                    SELECT setval('message_read_statuses_id_seq', COALESCE((SELECT MAX(id) FROM message_read_statuses), 1), false)
                """)
    op.execute("""
                    SELECT setval('messages_id_seq', COALESCE((SELECT MAX(id) FROM messages), 1), false)
                """)
    op.execute("""
                    SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1), false)
                """)
    users_table = sa.table('users',
                           sa.column('email', sa.String),
                           sa.column('hashed_password', sa.String),
                           sa.column('is_active', sa.Boolean),
                           sa.column('is_superuser', sa.Boolean),
                           sa.column('is_verified', sa.Boolean),
                           sa.column('name', sa.String),
                           )

    users_data = [
        {
            "email": "admin@admin.com",
            "hashed_password": pwd_context.hash("admin"),
            "is_active": True,
            "is_superuser": True,
            "is_verified": True,
            "name": "admin",
        },
        {
            "email": "TestUser1@TestUser1.com",
            "hashed_password": pwd_context.hash("TestUser1"),
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "name": "TestUser1",
        },
        {
            "email": "TestUser2@TestUser2.com",
            "hashed_password": pwd_context.hash("TestUser2"),
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "name": "TestUser2",
        },
        {
            "email": "TestUser3@TestUser3.com",
            "hashed_password": pwd_context.hash("TestUser3"),
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "name": "TestUser3",
        },
        {
            "email": "TestUser4@TestUser4.com",
            "hashed_password": pwd_context.hash("TestUser4"),
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "name": "TestUser4",
        },
    ]

    op.bulk_insert(users_table, users_data)

    groups_table = sa.table('groups',
                            sa.column('name', sa.String),
                            sa.column('creator_id', sa.Integer)
                            )

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

    op.bulk_insert(groups_table, groups)

    users_groups_table = sa.table('users_groups',
                                  sa.column('group_id', sa.Integer),
                                  sa.column('user_id', sa.Integer)
                                  )

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

    op.bulk_insert(users_groups_table, users_groups_connection)

    typechat_enum = sa.Enum('private', 'grouped', name='typechat', create_type=False)

    chats_table = sa.table('chats',
                           sa.column('name', sa.String),
                           sa.column('group_id', sa.Integer),
                           sa.column('type', typechat_enum),
                           )

    chats = [
        {
            'name': 'TestChat1',
            'group_id': 1,
            "type": 'private',
        },
        {
            'name': 'TestChat2',
            'group_id': 2,
            "type": 'grouped',
        },
    ]

    op.bulk_insert(chats_table, chats)


def downgrade() -> None:
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM groups")
    op.execute("DELETE FROM users_groups")
    op.execute("DELETE FROM chats")
    op.execute("""
            SELECT setval('chats_id_seq', COALESCE((SELECT MAX(id) FROM chats), 1), false)
        """)
    op.execute("""
                SELECT setval('groups_id_seq', COALESCE((SELECT MAX(id) FROM groups), 1), false)
            """)
    op.execute("""
                    SELECT setval('message_read_statuses_id_seq', COALESCE((SELECT MAX(id) FROM message_read_statuses), 1), false)
                """)
    op.execute("""
                    SELECT setval('messages_id_seq', COALESCE((SELECT MAX(id) FROM messages), 1), false)
                """)
    op.execute("""
                    SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1), false)
                """)
