from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import env

engine = create_async_engine(env().get_async_db_url(), echo=True)
async_session = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine,
    class_=AsyncSession
)

Base = declarative_base()

async def db():
    async with async_session() as session:
        yield session