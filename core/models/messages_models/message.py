from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, text, Boolean, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base


class Message(Base):
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content: Mapped[str] = mapped_column(String(1024), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    is_fully_read: Mapped[bool] = mapped_column(Boolean, default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
    read_statuses = relationship("MessageReadStatus", back_populates="message", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_message_read_status", "is_fully_read"),
        Index("idx_message_posted", "timestamp"),
        Index("idx_message_sender_timestamp", "sender_id", "timestamp")
    )