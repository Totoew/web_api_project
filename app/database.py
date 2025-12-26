from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Создаем асинхронный движок для SQLite
engine = create_async_engine(
    settings.database_url,
    echo=True,  # Логируем SQL-запросы (можно отключить в продакшене)
    future=True,
)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Функция для получения сессии БД (будет использоваться в зависимостях FastAPI)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session