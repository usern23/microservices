from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .repositories.UserRepository import UserRepository
from .repositories.ArticleRepository import ArticleRepository
from .repositories.CommentRepository import CommentRepository
from .controllers.users import UserController
from .controllers.articles import ArticleController
from .controllers.comments import CommentController as CommentCtrl


# Фабрика для создания контроллеров
async def get_user_controller(session: AsyncSession = Depends(get_session)):
    return UserController(UserRepository(session))

async def get_article_controller(session: AsyncSession = Depends(get_session)):
    return ArticleController(ArticleRepository(session), UserRepository(session))

async def get_comment_controller(session: AsyncSession = Depends(get_session)):
    return CommentCtrl(
        CommentRepository(session),
        ArticleRepository(session),
        UserRepository(session),
    )
