import uuid

from sqlalchemy import UUID, String, Uuid
from sqlalchemy.orm import mapped_column, Mapped


from app.db.postgresql import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=128), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(length=1024), nullable=False)
