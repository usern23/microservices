from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..schemas.articles import ArticleCreate, ArticleUpdate, Article
from ..schemas.users import User
from ..controllers.articles import ArticleController
from ..dependencies import get_article_controller
from ..auth import get_current_user

router = APIRouter(prefix="/api/articles", tags=["Articles"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    controller: ArticleController = Depends(get_article_controller),
):
    return await controller.create_article(article_data, current_user)

@router.get("", response_model=list[Article])
async def list_articles(
    skip: int = 0,
    limit: int = 20,
    controller: ArticleController = Depends(get_article_controller),
):
    return await controller.list_articles(skip, limit)

@router.get("/{slug}", response_model=Article)
async def get_article(
    slug: str,
    controller: ArticleController = Depends(get_article_controller),
):
    return await controller.get_article_by_slug(slug)

@router.put("/{slug}", response_model=Article)
async def update_article(
    slug: str,
    article_update: ArticleUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    controller: ArticleController = Depends(get_article_controller),
):
    return await controller.update_article(slug, article_update, current_user)

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    slug: str,
    current_user: Annotated[User, Depends(get_current_user)],
    controller: ArticleController = Depends(get_article_controller),
):
    await controller.delete_article(slug, current_user)
    return {"ok": True}
