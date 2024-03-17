from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


# Класс БД для таблицы с задачами
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger,
                                    primary_key=True,
                                    autoincrement=True
                                    )
    title: Mapped[str]
    description: Mapped[str]
    creation_time: Mapped[datetime] = mapped_column(DateTime,
                                                    nullable=False,
                                                    server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(DateTime,
                                               nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    username: Mapped[str]


# Класс БД для таблицы с пользователями
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger,
                                    primary_key=True,
                                    autoincrement=True
                                    )
    username: Mapped[str]
    password_hash: Mapped[str] = mapped_column((String(64)))
    salt: Mapped[str] = mapped_column(String(32))
