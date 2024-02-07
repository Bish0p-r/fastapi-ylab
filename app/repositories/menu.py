from typing import Sequence
from uuid import UUID

from sqlalchemy import RowMapping, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.common.base.repository import BaseRepository
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu


class MenuRepository(BaseRepository):
    model = Menu

    @classmethod
    async def get_one_or_none_with_counts(cls, session: AsyncSession, menu_id: UUID, **filter_by) -> RowMapping | None:
        query = (
            (
                select(
                    Menu.__table__.columns,
                    func.count(distinct(SubMenu.id)).label('submenus_count'),
                    func.count(distinct(Dish.id)).label('dishes_count'),
                )
                .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
                .outerjoin(Dish, Dish.submenu_id == SubMenu.id)
                .group_by(Menu.id)
            )
            .where(cls.model.id == menu_id)
            .filter_by(**filter_by)
        )
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def get_all_with_counts(cls, session: AsyncSession, **filter_by) -> Sequence[RowMapping]:
        query = (
            select(
                Menu.__table__.columns,
                func.count(distinct(SubMenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == SubMenu.id)
            .group_by(Menu.id)
        ).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def get_tree_list(cls, session: AsyncSession) -> Sequence[Menu]:
        query = select(Menu).options(selectinload(Menu.submenus).options(selectinload(SubMenu.dishes)))
        result = await session.execute(query)
        return result.scalars().all()
