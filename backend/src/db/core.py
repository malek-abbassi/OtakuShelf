"""
Database configuration and session management.
Handles SQLModel engine creation and session lifecycle.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlmodel import SQLModel, create_engine, Session

from ..config import get_settings

settings = get_settings()

# Create sync engine for development/testing with SQLite
engine = create_engine(
    settings.database_url,
    echo=settings.environment == "development",
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.database_url
    else {},
)

# For production, you might want to use async engine with PostgreSQL
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# async_engine = create_async_engine(
#     settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
#     echo=settings.environment == "development",
# )


def create_db_and_tables():
    """Create database tables based on SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """
    Dependency to get a database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


# For async operations (future enhancement)
@asynccontextmanager
async def get_async_session() -> AsyncGenerator[None, None]:
    """
    Async context manager for database sessions.

    Yields:
        AsyncSession: Async SQLModel database session
    """
    # Uncomment when moving to async
    # async with AsyncSession(async_engine) as session:
    #     yield session
    raise NotImplementedError("Async sessions not implemented yet")
