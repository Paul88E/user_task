from abc import ABC, abstractmethod

from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


# Абстрактный класс репозитория, описывающий комплект методов
class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, data: dict):
        raise NotImplementedError


# Конкретная реализация класса-репозитория
# с возможностью подстановки модели данных
class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update_one(self, data: dict):
        query = update(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_one(self, data: dict):
        query = delete(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()
