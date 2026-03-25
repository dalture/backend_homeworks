from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import declarative_base
from core.config import DB_URL

Base = declarative_base()
engine: AsyncEngine = create_async_engine(DB_URL)
AsyncSessionLocal = async_sessionmaker(autocommit=False, class_=AsyncSession, expire_on_commit=False, autoflush=False, bind=engine)

# Функция, которая создает подключение к БД. Используем как зависимость
async def get_db():
    with AsyncSessionLocal() as session:
        yield session