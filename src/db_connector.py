from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import settings


engine = create_async_engine(settings.DB_URL, echo=True, future=True)

AsyncSession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session():
    async with AsyncSession() as async_session:
        yield async_session
