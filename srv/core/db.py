from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import env

sync_engine = create_engine(env().get_sync_db_url(), echo=True)
async_engine = create_async_engine(env().get_async_db_url(), echo=True)
async_session = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = async_engine,
    class_=AsyncSession
    )

async def db():
    async with async_session() as session:
        yield session