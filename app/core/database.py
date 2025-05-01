from sqlalchemy import TypeDecorator, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import datetime
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()

class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def get_by_id(self, id: int):
        pass

    @abstractmethod
    async def create(self, entity):
        pass

class BaseService(ABC):
    def __init__(self, repository: BaseRepository):
        self._repo = repository
        
class UnixTimestamp(TypeDecorator):
    impl = BigInteger
    cache_ok = True
    def process_bind_param(self, value: datetime, _) -> int | None:
        return int(value.timestamp()) if value else None
    def process_result_value(self, value: int, _) -> int | None:
        return value
    
engine = create_async_engine(
    settings.db_url,
    echo=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()