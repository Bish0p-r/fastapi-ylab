from uuid import UUID

from sqlalchemy import select, func, distinct

from app.db.postgresql import async_session_maker
from app.common.base.repository import BaseRepository
from app.models.menu import Menu
from app.models.submenu import SubMenu
from app.models.dish import Dish


class MenuRepository(BaseRepository):
    model = Menu

    @classmethod
    async def get_one_or_none_with_counts(cls, menu_id: UUID, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(
                    Menu.__table__.columns,
                    func.count(distinct(SubMenu.id)).label("submenus_count"),
                    func.count(distinct(Dish.id)).label("dishes_count")
                )
                .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
                .outerjoin(Dish, Dish.submenu_id == SubMenu.id)
                .group_by(Menu.id)
            ).where(cls.model.id == menu_id).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all_with_counts(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(
                    Menu.__table__.columns,
                    func.count(distinct(SubMenu.id)).label("submenus_count"),
                    func.count(distinct(Dish.id)).label("dishes_count")
                )
                .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
                .outerjoin(Dish, Dish.submenu_id == SubMenu.id)
                .group_by(Menu.id)
            ).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
