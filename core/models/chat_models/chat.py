import enum

from sqlalchemy import String, Enum, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base


class TypeChat(enum.Enum):
    private = 'private'
    grouped = 'grouped'


class Chat(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[TypeChat] = mapped_column(Enum(TypeChat), nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)

    group = relationship("Group", back_populates="chat")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('id', 'group_id', name='unique_chat'),
        Index('ix_chat_group_id', 'group_id'),
        Index('ix_chat_type', 'type'),
    )
