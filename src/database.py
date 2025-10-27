import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Собираем URL для подключения к БД из отдельных переменных окружения
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

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Зависимость для получения сессии базы данных
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
