"""
Database Connection and Session Management
Handles PostgreSQL connection using SQLAlchemy
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
import os
from dotenv import load_dotenv

from backend.models import Base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection pieces (explicit host/port to avoid IPv6 localhost pitfalls)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "agentic_db")

# Database URLs (env overrides take precedence)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SYNC_DATABASE_URL = os.getenv(
    "SYNC_DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Remove SSL query parameters from asyncpg URL (asyncpg doesn't support them in URL)
if DATABASE_URL and "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

# Async Engine (for FastAPI async endpoints)
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={"ssl": "require"} if "neon.tech" in DATABASE_URL or "aws" in DATABASE_URL else {}
)

# Sync Engine (for tools that don't support async)
# Remove query params from SYNC_DATABASE_URL for psycopg2 compatibility
SYNC_URL_CLEAN = SYNC_DATABASE_URL.split("?")[0] if SYNC_DATABASE_URL and "?" in SYNC_DATABASE_URL else SYNC_DATABASE_URL

sync_engine = create_engine(
    SYNC_URL_CLEAN,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"sslmode": "require"} if "neon.tech" in SYNC_URL_CLEAN or "aws" in SYNC_URL_CLEAN else {}
)

# Session factories
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def init_db():
    """
    Initialize database tables
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_session() -> Session:
    """
    Get synchronous database session (for tools)
    """
    session = SyncSessionLocal()
    try:
        return session
    except Exception as e:
        session.close()
        raise


async def test_connection():
    """
    Test database connection
    """
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            # Just executing is enough to test connection
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}", exc_info=True)
        return False


@asynccontextmanager
async def get_db_session():
    """
    Context manager for database sessions
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
