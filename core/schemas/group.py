from datetime import datetime

from pydantic import BaseModel


class GroupBase(BaseModel):
    pass


class GroupCreate(GroupBase):
    name: str
    creator_id: int


class GroupRead(GroupCreate):
    id: int
    created_at: datetime
    updated_at: datetime
