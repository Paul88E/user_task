from pydantic_settings import BaseSettings


# Класс, считывающий настройки из файла .env
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    JWT_KEY: str
    JWT_ALGORITHM: str = "HS256"

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
