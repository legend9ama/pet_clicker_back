import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.modules.clicks.repository import ClickRepository

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(test_db_engine):
    async with sessionmaker(
        test_db_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest.fixture
def repo(db_session):
    return ClickRepository(db_session)