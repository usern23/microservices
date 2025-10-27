import uuid
from pydantic import BaseModel, Field

class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: list[str] = []

class ArticleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None

class ArticleBase(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: list[str]

    class Config:
        from_attributes = True

class UserForArticle(BaseModel):
    username: str
    bio: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True

class Article(ArticleBase):
    author: UserForArticle
