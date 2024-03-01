from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.abstract.repository.base import AbstractCRUDRepository


class AbstractSubMenuRepository(AbstractCRUDRepository, ABC):
    @classmethod
    @abstractmethod
    async def get_one_or_none_with_counts(
        cls, session: AsyncSession, menu_id: UUID, submenu_id: UUID, **filter_by
    ) -> RowMapping | None:
        ...

    @classmethod
    @abstractmethod
    async def get_all_with_counts(cls, session: AsyncSession, menu_id: UUID, **filter_by) -> Sequence[RowMapping]:
        ...
