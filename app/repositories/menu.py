from uuid import UUID

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base.repository import BaseRepository
from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import SubMenu


class MenuRepository(BaseRepository):
    model = Menu

    @classmethod
    async def get_one_or_none_with_counts(cls, session: AsyncSession, menu_id: UUID, **filter_by):
        query = (
            (
                select(
                    Menu.__table__.columns,
                    func.count(distinct(SubMenu.id)).label("submenus_count"),
                    func.count(distinct(Dish.id)).label("dishes_count"),
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
    async def get_all_with_counts(cls, session: AsyncSession, **filter_by):
        query = (
            select(
                Menu.__table__.columns,
                func.count(distinct(SubMenu.id)).label("submenus_count"),
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == SubMenu.id)
            .group_by(Menu.id)
        ).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().all()
