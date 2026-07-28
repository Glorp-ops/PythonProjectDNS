from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from ...core import settings

engine_null_pull = create_async_engine(settings.DB_URL, poolclass=NullPool, echo=False)
engine = create_async_engine(settings.DB_URL, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
async_session_null_pool = async_sessionmaker(
    engine_null_pull, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    async with async_session() as session:
        yield session
