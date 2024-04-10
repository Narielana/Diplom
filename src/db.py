from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+asyncpg://admin:postgres@localhost/auth'


async def get_db() -> AsyncSession: # type: ignore
    async with SessionLocal() as conn:
        yield conn


engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)
