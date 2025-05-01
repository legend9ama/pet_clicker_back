from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int):
        pass