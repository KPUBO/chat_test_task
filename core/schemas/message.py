from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.v1 import PrivateAttr


class MessageBase(BaseModel):
    pass


class MessageCreate(MessageBase):
    chat_id: int
    content: str


class MessageRead(MessageCreate):
    id: int
    sender_id: int
    timestamp: datetime
