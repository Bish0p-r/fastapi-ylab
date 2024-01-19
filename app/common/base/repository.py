from sqlalchemy import select, insert, delete, update

from app.db.postgresql import async_session_maker
from app.common.base.model import BaseModel


class BaseRepository:
    model: BaseModel = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            user_booked_rooms = delete(cls.model).filter_by(**filter_by).returning(cls.model.__table__.columns)
            result = await session.execute(user_booked_rooms)
            await session.commit()
            return result.mappings().one_or_none()

    @classmethod
    async def update(cls, data: dict, **filter_by):
        async with async_session_maker() as session:
            query = update(cls.model).values(**data).filter_by(**filter_by).returning(cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()
