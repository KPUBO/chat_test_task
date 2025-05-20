from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, Index

from core.models import Base

users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), index=True),
    Column("group_id", ForeignKey("groups.id"), index=True),
    UniqueConstraint('user_id', 'group_id', name='users_groups_unique'),
    Index("idx_users_groups_user", "user_id"),  # ← Добавить
    Index("idx_users_groups_group", "group_id"),  # ← Добавить
    Index("idx_users_groups_composite", "user_id", "group_id")  # ← Для JOIN
)
