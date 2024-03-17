from fastapi import FastAPI
import uvicorn

from app.api.endpoints import users_route, tasks_route

app = FastAPI()

app.include_router(users_route, prefix="/users")
app.include_router(tasks_route, prefix="/tasks")


if __name__ == "__main__":
    uvicorn.run("main:app")
