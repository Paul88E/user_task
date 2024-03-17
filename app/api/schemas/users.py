from pydantic import BaseModel, field_validator, constr


# Класс, используемый для регистрации и входа
class UserCreate(BaseModel):
    username: constr(max_length=40)
    password: constr(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value) -> str:
        if value.isalpha():
            raise ValueError("You should use some non-alphabet characters!")
        return value


# Класс, используемый для вывода данных из БД
class UserDB(BaseModel):
    id: int
    username: str
    password_hash: str
    salt: str


# Класс, используемый для передачи данных о пользователе и хэшированном пароле
class UserPwdSalt(BaseModel):
    username: str
    password_hash: str
    salt: str
