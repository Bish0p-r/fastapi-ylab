from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.models.dish import Dish


class AbstractDishServices(ABC):
    @abstractmethod
    async def list(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> Sequence[Dish]:
        ...

    @abstractmethod
    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> Dish:
        ...

    @abstractmethod
    async def create(
        self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, data: dict, background_tasks: BackgroundTasks
    ) -> RowMapping | None:
        ...

    @abstractmethod
    async def update(
        self,
        session: AsyncSession,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        data: dict,
        background_tasks: BackgroundTasks,
    ) -> RowMapping | None:
        ...

    @abstractmethod
    async def delete(
        self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID, background_tasks: BackgroundTasks
    ) -> JSONResponse:
        ...
