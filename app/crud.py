"""CRUD operations for tasks in the Task Tracker service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas

async def get_tasks(session: AsyncSession) -> list[models.Task]:
    """Retrieve all tasks from the database."""
    result = await session.execute(select(models.Task))
    return result.scalars().all()

async def get_task(session: AsyncSession, task_id: int) -> models.Task | None:
    """Retrieve a single task by its ID."""
    result = await session.execute(
        select(models.Task).where(models.Task.id == task_id)
    )
    return result.scalars().first()

async def create_task(session: AsyncSession, task_in: schemas.TaskCreate) -> models.Task:
    """Create a new task and persist it to the database."""
    task = models.Task(title=task_in.title, description=task_in.description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def update_task(
    session: AsyncSession, task: models.Task, task_in: schemas.TaskUpdate
) -> models.Task:
    """Update an existing task with new values."""
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.completed is not None:
        task.completed = task_in.completed
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(session: AsyncSession, task: models.Task) -> None:
    """Remove a task from the database."""
    await session.delete(task)
    await session.commit()
