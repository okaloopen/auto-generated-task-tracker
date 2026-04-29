"""Entry point and API routes for the Task Tracker service.

This module defines the FastAPI application, configures logging, and exposes
endpoints for CRUD operations on tasks. It uses asynchronous SQLAlchemy
sessions for database interactions and Pydantic models for data validation.
"""

from __future__ import annotations

import logging
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, database, schemas

app = FastAPI(title="Task Tracker API", version="0.1.0")

# Configure basic logging. In a production environment, logging should be
# configured to write to files or external systems.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize the database on application startup."""
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    logger.info("Database schema ensured.")


@app.get("/tasks", response_model=List[schemas.TaskRead])
async def read_tasks(session: AsyncSession = Depends(database.get_session)) -> List[schemas.TaskRead]:
    """Return a list of all tasks."""
    tasks = await crud.get_tasks(session)
    return tasks


@app.post(
    "/tasks",
    response_model=schemas.TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: schemas.TaskCreate, session: AsyncSession = Depends(database.get_session)
) -> schemas.TaskRead:
    """Create a new task."""
    task = await crud.create_task(session, task_in)
    return task


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
async def read_task(
    task_id: int, session: AsyncSession = Depends(database.get_session)
) -> schemas.TaskRead:
    """Retrieve a task by its ID."""
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
async def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    session: AsyncSession = Depends(database.get_session),
) -> schemas.TaskRead:
    """Update an existing task."""
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated = await crud.update_task(session, task, task_in)
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, session: AsyncSession = Depends(database.get_session)
) -> None:
    """Delete a task."""
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await crud.delete_task(session, task)
    return None
