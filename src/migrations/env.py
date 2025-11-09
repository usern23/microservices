from logging.config import fileConfig
import os
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio

config = context.config
fileConfig(config.config_file_name)

def _clean(v: str) -> str:
    if v is None:
        return v
    return (
        v.replace("\ufeff", "").replace("\u200b", "").replace("\xa0", "").strip()
    )

POSTGRES_USER = _clean(os.environ.get("POSTGRES_USER", "admin"))
POSTGRES_PASSWORD = _clean(os.environ.get("POSTGRES_PASSWORD", "admin"))
POSTGRES_HOST = _clean(os.environ.get("POSTGRES_HOST", "db"))
POSTGRES_PORT = _clean(os.environ.get("POSTGRES_PORT", "5432"))
POSTGRES_DB = _clean(os.environ.get("POSTGRES_DB", "mydatabase"))

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
config.set_main_option("sqlalchemy.url", DATABASE_URL)
print(f"[alembic] Using DB URL: {config.get_main_option('sqlalchemy.url')}")

from src.models.Base import Base
from src.models.Users import User
from src.models.Articles import Articles
from src.models.Comments import Comments

target_metadata = Base.metadata

def run_migrations_offline():
    print("[alembic] Running in OFFLINE mode")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    print("[alembic] Running in ONLINE mode (async)")
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
