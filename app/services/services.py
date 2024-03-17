import datetime

from app.api.schemas import TaskCreate, UserCreate, UserPwdSalt
from app.utils.unitofwork import IUnitOfWork
from app.core.security import user_hashed_password, jwt_generate

from fastapi.exceptions import HTTPException

JWT = str


# Service-класс для работы с БД
class UserTaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    # Функция добавления пользователя с выдачей токена
    async def add_user(self, user: UserCreate) -> JWT:
        """1. Проверяет наличие такого пользователя в базе данных.
           2. Если пользователь есть, вызывает ошибку и выводит соответствующее сообщение.
           3. Если пользователь новый - добавляет его в БД:
              генерирует соль, хэш на базе пароля и соли.
           """
        if user.username in await self.get_all_users():
            raise HTTPException(status_code=406, detail="User already exists")

        user_to_db: UserPwdSalt = await user_hashed_password(user)

        async with self.uow:
            await self.uow.user.create_one(user_to_db.model_dump())
            await self.uow.commit()

        return jwt_generate(user)

    # Функция выдачи всех пользователей из БД
    async def get_all_users(self):
        async with self.uow:
            users = await self.uow.user.read_all_users()
            return list(users)

    # Функция аутентификации пользователя с выдачей токена
    async def auth_user(self, user: UserCreate) -> str:
        async with self.uow:
            user_from_db: UserPwdSalt = await self.uow.user.read_one(user.username)

        if not user_from_db:
            raise HTTPException(status_code=403, detail="Invalid credentials")

        if user_from_db == await user_hashed_password(user, user_from_db.salt):
            return jwt_generate(user)

    # Функция создания новой задачи
    async def add_task(self, task: TaskCreate, user: str):
        task_data: dict = task.model_dump()
        task_data.update({"username": user})
        task_data.update({"creation_time": datetime.datetime.now()})
        async with self.uow:
            await self.uow.task.create_one(task_data)
            await self.uow.commit()

    # Функция выдачи всех задач пользователя
    async def get_all_tasks(self, user: str):
        async with self.uow:
            tasks = await self.uow.task.read_all(user)
            return tasks
