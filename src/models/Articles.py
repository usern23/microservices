from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from .Base import Base

class Articles(Base):
    
    __tablename__ = "Articles"

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True),primary_key=True)
    created_by : Mapped[UUID] = mapped_column(ForeignKey("Users.id"))
    title : Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    description : Mapped[str]
    body : Mapped[str]
    taglist: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    author = relationship("User", back_populates="articles")
    comments = relationship("Comments", back_populates="article", cascade="all, delete")