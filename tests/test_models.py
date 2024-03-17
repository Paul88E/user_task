import datetime

from app.api.schemas import UserCreate, TaskDB
import pytest


def test_user_create():
    user_data = {"username": "Norman",
                 "password": "norpass123"}
    user = UserCreate(**user_data)

    assert user.username == "Norman"
    assert user.password == "norpass123"

    with pytest.raises(ValueError):
        invalid_user_data = {"username": "Norman",
                             "password": "asdkjhhjhf"}
        invalid_user = UserCreate(**invalid_user_data)


def test_task_db():
    task_data = {"id": 1,
                 "title": "To fix car",
                 "description": "Go to service and fix car",
                 "deadline": "2024-04-16T18:30:00",
                 "username": "Alex",
                 "creation_time": "2024-04-15T18:30:00",
                 "completed": False}
    task_db = TaskDB(**task_data)

    assert task_db.title == "To fix car"
    assert type(task_db.deadline) == datetime.datetime



