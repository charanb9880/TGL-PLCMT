import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL")

engine: AsyncEngine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None

if DATABASE_URL:
    async_database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    engine = create_async_engine(
        async_database_url,
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=False,
        echo=False,
        connect_args={"statement_cache_size": 0, "command_timeout": 30},
    )
    async_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


def is_database_configured() -> bool:
    return bool(DATABASE_URL and engine)


async def get_db_session() -> AsyncSession:
    if async_session_factory is None:
        raise RuntimeError("DATABASE_URL is not configured")

    return async_session_factory()