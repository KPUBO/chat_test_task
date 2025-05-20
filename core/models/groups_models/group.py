from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, ForeignKey, text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.m2m_models.users_groups import users_groups


class Group(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))

    creator = relationship("User")
    chat = relationship("Chat", back_populates="group",  cascade="all, delete-orphan", uselist=False)

    participants: Mapped[List["User"]] = relationship(
        secondary=users_groups, back_populates="groups"
    )

    __table_args__ = (
        Index("idx_group_creator", "creator_id"),
    )