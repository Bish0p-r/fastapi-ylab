from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base.model import BaseModel


class BaseRepository:
    model: BaseModel = None

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def create(cls, session: AsyncSession, **data):
        query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        user_booked_rooms = delete(cls.model).filter_by(**filter_by).returning(cls.model.__table__.columns)
        result = await session.execute(user_booked_rooms)
        await session.commit()
        return result.mappings().one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, data: dict, **filter_by):
        query = update(cls.model).values(**data).filter_by(**filter_by).returning(cls.model.__table__.columns)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().one_or_none()
