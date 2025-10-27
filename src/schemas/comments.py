import uuid
from pydantic import BaseModel
from .users import User # Используем общую схему пользователя

# Схема для создания комментария
class CommentCreate(BaseModel):
    body: str

# Схема для отображения комментария
class Comment(BaseModel):
    id: uuid.UUID
    body: str
    author: User

    class Config:
        from_attributes = True
