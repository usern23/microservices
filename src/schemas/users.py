from pydantic import BaseModel, EmailStr

# Схема для регистрации пользователя
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Схема для аутентификации пользователя
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    bio: str | None = None
    image_url: str | None = None

# Схема для отображения данных пользователя в ответе
class User(BaseModel):
    username: str
    email: EmailStr
    bio: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True

# Схема для JWT токена
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
