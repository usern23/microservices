from fastapi import HTTPException, status
from ..schemas.articles import ArticleCreate, ArticleUpdate, Article, UserForArticle
from ..schemas.users import User
from ..repositories.ArticleRepository import ArticleRepository
from ..repositories.UserRepository import UserRepository
import uuid

class ArticleController:
    def __init__(self, article_repo: ArticleRepository, user_repo: UserRepository):
        self.article_repo = article_repo
        self.user_repo = user_repo

    async def create_article(self, article_data: ArticleCreate, current_user: User):
        user = await self.user_repo.get_by_username(current_user.username)
        if not user:
            raise HTTPException(status_code=404, detail="Author not found")
        
        payload = article_data.model_dump()
        if "tagList" in payload:
            payload["taglist"] = payload.pop("tagList")
        created = await self.article_repo.create(author_id=user.id, **payload)
        db_article = await self.article_repo.get_by_slug(created.slug)
        return self._to_schema(db_article).model_dump()

    async def get_article_by_slug(self, slug: str):
        db_article = await self.article_repo.get_by_slug(slug)
        if not db_article:
            raise HTTPException(status_code=404, detail="Article not found")
        return self._to_schema(db_article).model_dump()
        
    async def list_articles(self, skip: int, limit: int):
        articles = await self.article_repo.get_all(skip, limit)
        return [self._to_schema(article).model_dump() for article in articles]

    async def update_article(self, slug: str, article_update: ArticleUpdate, current_user: User):
        db_article = await self.article_repo.get_by_slug(slug)
        user = await self.user_repo.get_by_username(current_user.username)

        if not db_article:
            raise HTTPException(status_code=404, detail="Article not found")
        if db_article.created_by != user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        update_data = article_update.model_dump(exclude_unset=True)
        if "tagList" in update_data:
            update_data["taglist"] = update_data.pop("tagList")
        updated_article = await self.article_repo.update(db_article, **update_data)

        return self._to_schema(updated_article).model_dump()

    async def delete_article(self, slug: str, current_user: User):
        db_article = await self.article_repo.get_by_slug(slug)
        user = await self.user_repo.get_by_username(current_user.username)

        if not db_article:
            raise HTTPException(status_code=404, detail="Article not found")
        if db_article.created_by != user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        await self.article_repo.delete_article(db_article)
        return {"detail": "Article deleted successfully"}

    def _to_schema(self, a) -> Article:
        author = a.author
        author_schema = UserForArticle(
            username=author.username,
            bio=author.bio,
            image_url=author.image_url,
        ) if author is not None else UserForArticle(username="", bio=None, image_url=None)
        return Article(
            slug=a.slug,
            title=a.title,
            description=a.description,
            body=a.body,
            tagList=a.taglist or [],
            author=author_schema,
        )
