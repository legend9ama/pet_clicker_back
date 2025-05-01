from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository(ABC):
    def __init__(self, db: AsyncSession):
        self._db = db