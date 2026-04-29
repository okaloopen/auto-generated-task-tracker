"""Pydantic models (schemas) for the Task Tracker API.

These classes define the shape of data accepted and returned by the API.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base properties shared by task create and update operations."""

    title: str = Field(..., example="Buy groceries")
    description: str | None = Field(None, example="Milk, eggs, bread")


class TaskCreate(TaskBase):
    """Schema for creating a new task. Inherits all fields from ``TaskBase``."""
    pass


class TaskRead(TaskBase):
    """Schema for reading task information from the API."""

    id: int
    completed: bool

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    Fields are optional to allow partial updates.
    """

    title: str | None = Field(None, example="Clean the house")
    description: str | None = Field(None, example="Living room, kitchen")
    completed: bool | None = Field(None, example=True)
