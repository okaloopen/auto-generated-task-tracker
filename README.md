# Task Tracker API

Task Tracker API — это асинхронный веб‑сервис для управления задачами, созданный на базе FastAPI, SQLAlchemy (async) и SQLite. Сервис поддерживает операции создания, чтения, обновления и удаления задач (CRUD) через REST‑интерфейс. Архитектура проекта модульная и разделяет слои: инициализация приложения (`main.py`), настройка базы (`database.py`), ORM‑модели (`models.py`), Pydantic‑схемы (`schemas.py`) и CRUD‑операции (`crud.py`).

## Особенности

- Асинхронная работа с БД через aiosqlite.
- Чистая архитектура с разделением ответственности.
- Логирование событий через стандартный модуль `logging`.
- Перенастраиваемая СУБД (SQLite по умолчанию, легко сменить на PostgreSQL и др.).

## Установка

```bash
pip install -r requirements.txt
uvicorn task_tracker.app.main:app --reload
```

## API Documentation

| Метод | Путь | Описание |
| --- | --- | --- |
| GET | /tasks | Список задач |
| POST | /tasks | Создать задачу |
| GET | /tasks/{id} | Получить задачу |
| PUT | /tasks/{id} | Обновить задачу |
| DELETE | /tasks/{id} | Удалить задачу |

Более подробная документация доступна в Swagger UI (`/docs`).
