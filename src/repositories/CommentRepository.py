from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..models.Comments import Comments
import uuid
from .base import BaseRepository

class CommentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Comments)

    async def create(self, article_id: uuid.UUID, author_id: uuid.UUID, body: str) -> Comments:
        new_comment = Comments(
            id=uuid.uuid4(),
            article_id=article_id,
            created_by=author_id,
            body=body
        )
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment

    async def get_by_article_slug(self, article_id: uuid.UUID) -> list[Comments]:
        stmt = (
            select(self.model)
            .where(self.model.article_id == article_id)
            .options(selectinload(self.model.author))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_comment_by_id(self, comment_id: uuid.UUID) -> Comments | None:
        stmt = (
            select(self.model)
            .where(self.model.id == comment_id)
            .options(selectinload(self.model.author))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
