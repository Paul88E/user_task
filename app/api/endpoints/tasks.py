from fastapi import APIRouter, Request, Depends, HTTPException

from app.api.schemas import TaskCreate
from .users import get_user_task_service
from app.services import UserTaskService
from app.core.security import get_user_from_token

tasks_route = APIRouter()


# Функция проверки токена с выдачей имени пользователя
async def check_token(request: Request) -> str:
    user = ""
    try:
        token = request.headers["Authorization"]
        if token:
            user = await get_user_from_token(token)
    except KeyError:
        raise HTTPException(status_code=403, detail="Wrong token")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Конечная точка для создания задачи
@tasks_route.post("/create")
async def task_create(new_task: TaskCreate,
                      request: Request,
                      user_task_service: UserTaskService = Depends(get_user_task_service)):
    user = await check_token(request)
    await user_task_service.add_task(new_task, user)
    return {"message": f"Task '{new_task.title}' has been created"}


# Конечная точка для вывода всех задач пользователя
@tasks_route.get("/read")
async def task_get_all(request: Request,
                       user_task_service: UserTaskService = Depends(get_user_task_service)):
    user = await check_token(request)
    tasks = await user_task_service.get_all_tasks(user)
    return tasks
