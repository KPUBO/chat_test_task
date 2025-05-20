from pydantic import BaseModel

from core.models.chat_models.chat import TypeChat


class ChatBase(BaseModel):
    pass


class ChatCreate(ChatBase):
    name: str
    type: TypeChat
    group_id: int


class ChatRead(ChatBase):
    id: int
    name: str
    type: TypeChat
    group_id: int
