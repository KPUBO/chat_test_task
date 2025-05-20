from sqlalchemy import Integer, Column, ForeignKey, Boolean, DateTime, Index
from sqlalchemy.orm import relationship

from core.models import Base


class MessageReadStatus(Base):
    __tablename__ = 'message_read_statuses'

    message_id = Column(Integer, ForeignKey("messages.id"), primary_key=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    message = relationship("Message", back_populates="read_statuses")

    __table_args__ = (
        Index('ix_message_user', 'message_id', 'recipient_id'),
        Index('ix_read_status', 'is_read')
    )
