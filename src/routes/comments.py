from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..schemas.comments import CommentCreate, Comment
from ..schemas.users import User
from ..controllers.comments import CommentController
from ..dependencies import get_comment_controller
from ..auth import get_current_user
import uuid

router = APIRouter(prefix="/api/articles/{slug}/comments", tags=["Comments"])

@router.post("", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def add_comment_to_article(
    slug: str,
    comment_data: CommentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    controller: CommentController = Depends(get_comment_controller),
):
    return await controller.add_comment_to_article(slug, comment_data, current_user)

@router.get("", response_model=list[Comment])
async def get_comments_for_article(
    slug: str,
    controller: CommentController = Depends(get_comment_controller),
):
    return await controller.get_comments_for_article(slug)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    slug: str,
    comment_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    controller: CommentController = Depends(get_comment_controller),
):
    await controller.delete_comment(slug, comment_id, current_user)
    return {"ok": True}
