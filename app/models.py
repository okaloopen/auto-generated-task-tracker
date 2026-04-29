"""SQLAlchemy ORM models for the Task Tracker service."""

from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Task(Base):
    """Represents a task item in the database.

    Attributes:
        id: Primary key identifier for the task.
        title: Short title describing the task.
        description: Optional longer description of the task.
        completed: Boolean flag indicating whether the task is complete.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(length=1024), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
