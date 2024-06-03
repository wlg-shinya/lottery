from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "postgres+asyncpg://postgres:postgres@localhost:8502/lottery"

engine = create_async_engine(DB_URL, echo=True)
session = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with session() as session:
        yield session