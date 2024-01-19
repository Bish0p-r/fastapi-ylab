from uuid import UUID

from sqlalchemy import select, func, distinct

from app.db.postgresql import async_session_maker
from app.common.base.repository import BaseRepository
from app.models.submenu import SubMenu
from app.models.dish import Dish


class SubMenuRepository(BaseRepository):
    model = SubMenu

    @classmethod
    async def get_one_or_none_with_counts(cls, menu_id: UUID, submenu_id: UUID, **filter_by):
        async with async_session_maker() as session:
            query = (
                (
                    select(SubMenu.__table__.columns, func.count(distinct(Dish.id)).label("dishes_count"))
                    .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
                    .filter(SubMenu.menu_id == menu_id)
                    .group_by(SubMenu.id)
                )
                .where(cls.model.id == submenu_id)
                .filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all_with_counts(cls, menu_id: UUID, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(SubMenu.__table__.columns, func.count(distinct(Dish.id)).label("dishes_count"))
                .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
                .filter(SubMenu.menu_id == menu_id)
                .group_by(SubMenu.id)
            ).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
