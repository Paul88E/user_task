import jwt
import hashlib
import secrets

from fastapi import HTTPException, status
from .config import settings

from app.api.schemas import UserCreate, UserPwdSalt


# Функция генерации токена по имени пользователя и паролю
def jwt_generate(user_data: UserCreate) -> str:
    sub: dict = {"sub": user_data.model_dump()}
    jwt_token: jwt.PyJWT = jwt.encode(sub,
                                      key=settings.JWT_KEY,
                                      algorithm=settings.JWT_ALGORITHM)
    return str(jwt_token)


# Функция, извлекающая имя пользователя из токена
async def get_user_from_token(token: str) -> str:
    try:
        user_data = jwt.decode(token,
                               key=settings.JWT_KEY,
                               algorithms=settings.JWT_ALGORITHM)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong token",
                            headers={"WWW-Authenticate": "Bearer"})
    if user_data.get("sub"):
        return user_data["sub"].get("username")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# Функция, генерирующая соль и хэшированный пароль
async def user_hashed_password(user: UserCreate,
                               salt: str = secrets.token_hex(16)) -> UserPwdSalt:
    password_bytes: bytes = user.password.encode('utf-8')
    salt_bytes: bytes = salt.encode('utf-8')

    salted_password: bytes = password_bytes + salt_bytes
    hashed_password: str = hashlib.sha256(salted_password).hexdigest()
    user_to_db: UserPwdSalt = UserPwdSalt(username=user.username,
                                          password_hash=hashed_password,
                                          salt=salt)
    return user_to_db
