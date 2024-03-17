from sqlalchemy import select

from app.db import User
from app.api.schemas import UserPwdSalt
from app.repositories import Repository


# Класс БД для работы с таблицей пользователей
class UserRepository(Repository):
    model = User

    async def read_all_users(self) -> list[str]:
        result = await self.session.execute(select(self.model.username))
        users: list[str] = list(user[0] for user in result)
        return users

    async def read_one(self, username: str) -> UserPwdSalt:
        result = await self.session.execute(select(self.model.username,
                                                   self.model.password_hash,
                                                   self.model.salt).where(self.model.username == username))
        user_data_list: list[str] = list(*result)
        if user_data_list:
            user_data: UserPwdSalt = UserPwdSalt(username=user_data_list[0],
                                                 password_hash=user_data_list[1],
                                                 salt=user_data_list[2])
            return user_data
