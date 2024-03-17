from fastapi import APIRouter, Response, Depends

from app.api.schemas import UserCreate
from app.services import UserTaskService
from app.utils import IUnitOfWork, UnitOfWork

users_route = APIRouter()


# Функция, выдающая экземпляр БД типа "service"
def get_user_task_service(uow: IUnitOfWork =
                          Depends(UnitOfWork)) -> UserTaskService:
    return UserTaskService(uow)


# Конечная точка для регистрации пользователя с выдачей токена
@users_route.post("/registration")
async def user_register(user_data: UserCreate,
                        user_task_service: UserTaskService = Depends(get_user_task_service)):
    token = await user_task_service.add_user(user_data)
    return Response(headers={"Authorisation": token})


# Конечная точка для входа в систему с выдачей токена
@users_route.post("/login")
async def user_login(user: UserCreate,
                     user_task_service: UserTaskService = Depends(get_user_task_service)):
    token = await user_task_service.auth_user(user)
    return Response(headers={"Authorisation": token})
