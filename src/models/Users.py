from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .Base import Base

class User(Base):

    __tablename__ = "Users"

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email : Mapped[str]
    username : Mapped[str]
    password : Mapped[str]
    bio: Mapped[str | None]
    image_url: Mapped[str | None]

    articles = relationship("Articles", back_populates="author", cascade="all, delete")
    comments = relationship("Comments", back_populates="author", cascade="all, delete")
    