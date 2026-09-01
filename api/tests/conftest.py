import anyio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.database import Base, get_db
from src.item import Item  # noqa: F401
from src.main import app

# database connection
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingAsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# database setup for tests
@pytest.fixture(autouse=True)
def setup_test_database():
    async def create_schema() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_schema() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    anyio.run(create_schema)
    yield
    anyio.run(drop_schema)


# test client
@pytest.fixture
def client():
    async def override_get_db():
        async with TestingAsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
