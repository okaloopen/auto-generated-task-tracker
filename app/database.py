"""Database configuration and session management for the Task Tracker service.

This module defines the asynchronous SQLAlchemy engine and sessionmaker for
interaction with a SQLite database using the aiosqlite driver. It also
exposes a dependency that can be used in FastAPI endpoints to acquire an
``AsyncSession`` instance.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

# SQLite database URL using the aiosqlite driver. The database file will be
# created in the working directory as ``tasks.db``.
DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

# Create an asynchronous engine. ``echo=False`` disables verbose SQL logging.
engine = create_async_engine(DATABASE_URL, echo=False)

# Configure a sessionmaker factory for producing AsyncSession objects. We set
# ``expire_on_commit=False`` so that attributes remain available after commit.
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

# Base class for declarative models. All ORM models should inherit from this
# class.
Base = declarative_base()

async def get_session() -> AsyncSession:
    """Dependency that provides a transactional scope for database operations.

    Yields an ``AsyncSession`` bound to the configured engine. When the caller
    finishes with the session, it is automatically closed.
    """
    async with async_session() as session:
        yield session
