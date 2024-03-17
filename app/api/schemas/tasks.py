from pydantic import BaseModel
from datetime import datetime


# Класс, используемый для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    username: str


# Класс, используемый для вывода данных о задаче из БД
class TaskDB(TaskCreate):
    id: int
    creation_time: datetime = datetime.now()
    completed: bool = False
