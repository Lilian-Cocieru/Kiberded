# C:\Users\Computer\Desktop\python\Kiberded\alembic\env.py
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- НОВЫЕ ИМПОРТЫ ---
import asyncio  # Добавляем импорт asyncio
from sqlalchemy.ext.asyncio import AsyncEngine # Добавляем импорт AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
# 1. Импортируем Base из вашего engine.py
from database.engine import Base 

# 2. Импортируем *все* ваши классы моделей из database.models
from database.models import AIModel, Lesson, Task, VoiceMessage, User, Payment

# !!! НОВОЕ ДОБАВЛЕНИЕ !!!
# Импортируем переменные из вашего config.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    (Этот режим вам, скорее всего, не понадобится для этого проекта)
    """
    url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- САМЫЕ ВАЖНЫЕ ИЗМЕНЕНИЯ ЗДЕСЬ ---
def do_run_migrations(connection):
    context.configure(
        connection=connection, target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    В этом режиме мы создаем движок с помощью URL из config.py
    """
    connectable_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Создаем асинхронный движок через create_async_engine
    connectable = create_async_engine(connectable_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    # запускаем асинхронную функцию с asyncio.run()
    asyncio.run(run_migrations_online())
