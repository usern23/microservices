from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .Base import Base

class Comments(Base):

    __tablename__ = "Comments"

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key=True)
    article_id: Mapped[UUID] = mapped_column(ForeignKey("Articles.id"))
    created_by : Mapped[UUID] = mapped_column(ForeignKey("Users.id"))
    body : Mapped[str] = mapped_column()

    author = relationship("User", back_populates="comments")
    article = relationship("Articles", back_populates="comments")