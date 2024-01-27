from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.schemas.dish import DishSchema
from app.schemas.menu import MenuWithCountsSchema
from app.schemas.submenu import SubMenuWithCountSchema


async def is_menu_fields_equal(menu_id: str | UUID, response_data: dict, session: AsyncSession) -> bool:
    menu = await MenuRepository.get_one_or_none_with_counts(session=session, menu_id=menu_id)
    if menu is None:
        return False

    data = MenuWithCountsSchema(**response_data)

    for field in response_data:
        if getattr(menu, field) != getattr(data, field):
            return False
    return True


async def is_submenu_fields_equal(
    menu_id: str | UUID, submenu_id: str | UUID, response_data: dict, session: AsyncSession
) -> bool:
    submenu = await SubMenuRepository.get_one_or_none_with_counts(
        session=session, menu_id=menu_id, submenu_id=submenu_id
    )
    if submenu is None:
        return False

    data = SubMenuWithCountSchema(**response_data)

    for field in response_data:
        if getattr(submenu, field) != getattr(data, field):
            return False
    return True


async def is_dish_fields_equal(
    menu_id: str | UUID, submenu_id: str | UUID, dish_id: str | UUID, response_data: dict, session: AsyncSession
) -> bool:
    dish = await DishRepository.get_one_or_none(
        session=session, dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id
    )
    if dish is None:
        return False

    data = DishSchema(**response_data)

    for field in response_data:
        if getattr(dish, field) != getattr(data, field):
            return False
    return True


async def count_menus(session: AsyncSession, **kwargs) -> int:
    return len(await MenuRepository.get_all(session=session, **kwargs))


async def count_submenus(session: AsyncSession, menu_id: str | UUID, **kwargs) -> int:
    return len(await SubMenuRepository.get_all(session=session, menu_id=menu_id, **kwargs))


async def count_dishes(session: AsyncSession, menu_id: str | UUID, submenu_id: str | UUID, **kwargs) -> int:
    return len(await DishRepository.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id, **kwargs))
