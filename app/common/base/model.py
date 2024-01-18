from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped


from app.db.postgresql import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)

    # id: Mapped[int] = mapped_column(primary_key=True)

    # id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    # title: Mapped[str] = mapped_column(String(length=128), unique=True, nullable=False)
    # description: Mapped[str] = mapped_column(String(length=1024), nullable=False)
