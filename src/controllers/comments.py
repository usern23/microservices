from fastapi import HTTPException, status
from ..schemas.comments import CommentCreate, Comment
from ..schemas.users import User
from ..repositories.CommentRepository import CommentRepository
from ..repositories.ArticleRepository import ArticleRepository
from ..repositories.UserRepository import UserRepository
import uuid

class CommentController:
    def __init__(
        self,
        comment_repo: CommentRepository,
        article_repo: ArticleRepository,
        user_repo: UserRepository,
    ):
        self.comment_repo = comment_repo
        self.article_repo = article_repo
        self.user_repo = user_repo

    async def add_comment_to_article(self, slug: str, comment_data: CommentCreate, current_user: User) -> Comment:
        article = await self.article_repo.get_by_slug(slug)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        user = await self.user_repo.get_by_username(current_user.username)
        if not user:
            raise HTTPException(status_code=404, detail="Author not found")
        
        db_comment = await self.comment_repo.create(
            article_id=article.id,
            author_id=user.id,
            body=comment_data.body
        )
        # Нужно пересобрать объект, чтобы автор был подгружен
        db_comment = await self.comment_repo.get_comment_by_id(db_comment.id)
        return Comment.model_validate(db_comment)

    async def get_comments_for_article(self, slug: str) -> list[Comment]:
        article = await self.article_repo.get_by_slug(slug)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        comments = await self.comment_repo.get_by_article_slug(article.id)
        return [Comment.model_validate(comment) for comment in comments]

    async def delete_comment(self, comment_id: uuid.UUID, current_user: User):
        comment = await self.comment_repo.get_comment_by_id(comment_id)
        user = await self.user_repo.get_by_username(current_user.username)

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.created_by != user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        await self.comment_repo.delete(comment)
        return {"detail": "Comment deleted successfully"}
