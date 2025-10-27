from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.Users import User
import uuid

from .base import BaseRepository 

class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = User

    async def create(self, username: str, email: str, hashed_password: str) -> User:
        new_user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
