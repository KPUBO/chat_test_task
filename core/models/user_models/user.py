from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import text, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.m2m_models.users_groups import users_groups


class User(Base, SQLAlchemyBaseUserTable[int]):
    name: Mapped[str] = mapped_column(String, unique=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))

    messages = relationship("Message", back_populates="sender")

    groups: Mapped[List["Group"]] = relationship(
        secondary=users_groups, back_populates="participants"
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)