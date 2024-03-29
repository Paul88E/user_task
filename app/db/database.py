from sqlalchemy.ext.asyncio import AsyncSession,\
    create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


# Абстрактный класс базы данных для последующего наследования
class Base(DeclarativeBase):
    pass


# Функция, выдающая экземпляр сессии
async def get_async_session():
    async with async_session_maker() as session:
        yield session
