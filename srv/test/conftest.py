import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import env
from core.db import db
from api.models import Base
from api.main import app

@pytest.fixture
async def client_generator() -> AsyncGenerator[AsyncClient, None]:
    async_engine = create_async_engine(env().get_async_db_url(env().db_test_url), echo=True)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def db_test():
        async with async_session() as session:
            yield session
    
    app.dependency_overrides[db] = db_test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client