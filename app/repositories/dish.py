from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base.repository import BaseRepository
from app.models.dish import Dish
from app.models.submenu import SubMenu


class DishRepository(BaseRepository):
    model = Dish

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID, **filter_by):
        query = (
            select(cls.model.__table__.columns)
            .join(SubMenu, cls.model.submenu_id == SubMenu.id)
            .where(cls.model.submenu_id == submenu_id, SubMenu.menu_id == menu_id, cls.model.id == dish_id)
        ).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession, menu_id: UUID, submenu_id: UUID, **filter_by):
        query = (
            select(cls.model.__table__.columns)
            .join(SubMenu, cls.model.submenu_id == SubMenu.id)
            .where(cls.model.submenu_id == submenu_id, SubMenu.menu_id == menu_id)
        ).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()
