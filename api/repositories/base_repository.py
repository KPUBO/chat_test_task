from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Sequence

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    async def get_all(self) -> Sequence[T]:
        pass

    @abstractmethod
    async def get_by_id(self, item_id) -> Optional[T]:
        pass

    @abstractmethod
    async def insert_item(self, item: T) -> T:
        pass

    @abstractmethod
    async def update_item(self, item_id, item: T) -> Optional[T]:
        pass

    @abstractmethod
    async def delete_by_id(self, item_id) -> Optional[T]:
        pass
