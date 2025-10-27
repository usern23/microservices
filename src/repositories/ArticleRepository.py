from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..models.Articles import Articles
import uuid
from .base import BaseRepository
from slugify import slugify

class ArticleRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Articles)

    async def _generate_unique_slug(self, title: str, exclude_id: uuid.UUID | None = None) -> str:
        base = slugify(title)
        stmt = select(self.model.slug)
        like_expr = f"{base}%"
        if exclude_id is not None:
            stmt = stmt.where(self.model.slug.like(like_expr), self.model.id != exclude_id)
        else:
            stmt = stmt.where(self.model.slug.like(like_expr))
        result = await self.session.execute(stmt)
        existing = {row[0] for row in result.fetchall()}
        slug = base
        i = 1
        while slug in existing:
            slug = f"{base}-{i}"
            i += 1
        return slug

    async def create(self, author_id: uuid.UUID, **kwargs) -> Articles:
        slug = await self._generate_unique_slug(kwargs["title"])  # уникальный слаг
        new_article = Articles(
            id=uuid.uuid4(),
            created_by=author_id,
            slug=slug,
            **kwargs
        )
        self.session.add(new_article)
        await self.session.commit()
        await self.session.refresh(new_article)
        return new_article

    async def get_by_slug(self, slug: str) -> Articles | None:
        stmt = select(self.model).where(self.model.slug == slug).options(selectinload(self.model.author))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Articles]:
        stmt = select(self.model).offset(skip).limit(limit).options(selectinload(self.model.author))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, article: Articles, **kwargs) -> Articles:
        if "title" in kwargs:
            kwargs["slug"] = await self._generate_unique_slug(kwargs["title"], exclude_id=article.id)

        for key, value in kwargs.items():
            setattr(article, key, value)
        
        await self.session.commit()
        await self.session.refresh(article)
        return article

    async def delete_article(self, article: Articles):
        await self.session.delete(article)
        await self.session.commit()
