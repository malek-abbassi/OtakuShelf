"""
Database configuration and session management.
Handles SQLModel engine creation and session lifecycle.
"""

import logging
from contextlib import asynccontextmanager
from typing import Generator, AsyncGenerator

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import QueuePool

from ..config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

# Production-ready engine configuration
engine_kwargs = {
    "echo": settings.environment == "development",
    "pool_pre_ping": True,  # Verify connections before use
    "pool_recycle": 3600,  # Recycle connections after 1 hour
}

# Database-specific configurations
if "sqlite" in settings.database_url:
    # SQLite specific settings
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": None,  # SQLite doesn't use connection pooling
    })
else:
    # PostgreSQL/MySQL production settings
    engine_kwargs.update({
        "pool_size": 10,  # Number of connections to maintain
        "max_overflow": 20,  # Maximum additional connections
        "poolclass": QueuePool,
        "pool_timeout": 30,  # Timeout for getting connection from pool
    })

# Create sync engine with production optimizations
engine = create_engine(settings.database_url, **engine_kwargs)

# Enable SQLAlchemy query logging in development
if settings.environment == "development":
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Connection pool monitoring
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    """Log database connections."""
    logger.debug("Database connection established")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    """Log connection checkouts."""
    logger.debug("Database connection checked out from pool")

@event.listens_for(engine, "checkin")
def checkin(dbapi_connection, connection_record):
    """Log connection checkins."""
    logger.debug("Database connection returned to pool")


def create_db_and_tables():
    """Create database tables based on SQLModel metadata."""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


# For async operations (future enhancement)
@asynccontextmanager
async def get_async_session() -> AsyncGenerator[Session, None]:
    """
    Async context manager for database sessions.

    Yields:
        AsyncSession: Async SQLModel database session
    """
    # Uncomment when moving to async
    # async with AsyncSession(async_engine) as session:
    #     yield session
    raise NotImplementedError("Async sessions not implemented yet")
