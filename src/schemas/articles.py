import uuid
from pydantic import BaseModel, Field

# Схема для создания статьи
class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: list[str] = []

# Схема для обновления статьи
class ArticleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None

# Базовая схема для отображения статьи (без вложенных объектов)
class ArticleBase(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: list[str]

    class Config:
        from_attributes = True

# Схема для отображения пользователя внутри статьи
class UserForArticle(BaseModel):
    username: str
    bio: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True

# Финальная схема для отображения статьи с автором
class Article(ArticleBase):
    author: UserForArticle
