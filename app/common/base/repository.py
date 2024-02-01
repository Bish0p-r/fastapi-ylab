from typing import Sequence

from sqlalchemy import RowMapping, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql import Base


class BaseRepository:
    model: type[Base]

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by) -> RowMapping | None:
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, **filter_by) -> Sequence[RowMapping]:
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def create(cls, session: AsyncSession, **data) -> RowMapping | None:
        query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by) -> RowMapping | None:
        user_booked_rooms = delete(cls.model).filter_by(**filter_by).returning(cls.model.__table__.columns)
        result = await session.execute(user_booked_rooms)
        await session.commit()
        return result.mappings().one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, data: dict, **filter_by) -> RowMapping | None:
        query = update(cls.model).values(**data).filter_by(**filter_by).returning(cls.model.__table__.columns)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().one_or_none()
