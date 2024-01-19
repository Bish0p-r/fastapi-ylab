from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings


async_engine = create_async_engine(settings.db_uri, echo=True)
async_session_maker = sessionmaker(bind=async_engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
