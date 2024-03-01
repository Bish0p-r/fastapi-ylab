from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.abstract.repository.base import AbstractCRUDRepository
from app.models.dish import Dish


class AbstractDishRepository(AbstractCRUDRepository, ABC):
    @classmethod
    @abstractmethod
    async def get_one_or_none_dish(
        cls, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID, **filter_by
    ) -> Dish | None:
        ...

    @classmethod
    @abstractmethod
    async def get_all_dishes(
        cls, session: AsyncSession, menu_id: UUID, submenu_id: UUID, **filter_by
    ) -> Sequence[Dish]:
        ...
