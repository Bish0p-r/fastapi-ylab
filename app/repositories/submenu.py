from typing import Sequence
from uuid import UUID

from sqlalchemy import RowMapping, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base.repository import BaseRepository
from app.models.dish import Dish
from app.models.submenu import SubMenu


class SubMenuRepository(BaseRepository):
    model = SubMenu

    @classmethod
    async def get_one_or_none_with_counts(
        cls, session: AsyncSession, menu_id: UUID, submenu_id: UUID, **filter_by
    ) -> RowMapping | None:
        query = (
            (
                select(SubMenu.__table__.columns, func.count(distinct(Dish.id)).label('dishes_count'))
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
    async def get_all_with_counts(cls, session: AsyncSession, menu_id: UUID, **filter_by) -> Sequence[RowMapping]:
        query = (
            select(SubMenu.__table__.columns, func.count(distinct(Dish.id)).label('dishes_count'))
            .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
            .filter(SubMenu.menu_id == menu_id)
            .group_by(SubMenu.id)
        ).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()
