from sqlalchemy import select, insert

from app.db import Task
from app.repositories import Repository


# Класс БД для работы с таблицей задач
class TaskRepository(Repository):
    model = Task

    async def create_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def read_all(self, user: str) -> list[list]:
        result = await self.session.execute(select(self.model.id,
                                                   self.model.title,
                                                   self.model.description,
                                                   self.model.creation_time,
                                                   self.model.deadline,
                                                   self.model.username)
                                            .where(self.model.username == user))
        tasks = list(list(user) for user in result.fetchall())
        if tasks:
            return tasks
