from typing import Sequence
from uuid import UUID

from fastapi.responses import JSONResponse
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import DishNotFound, DishWithThisTitleExists
from app.repositories.dish import DishRepository


class DishServices:
    def __init__(self, repository: type[DishRepository]):
        self.repository = repository

    async def list(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> Sequence[RowMapping]:
        return await self.repository.get_all_dishes(session=session, menu_id=menu_id, submenu_id=submenu_id)

    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> RowMapping:
        result = await self.repository.get_one_or_none_dish(
            session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        if result is None:
            raise DishNotFound
        return result

    async def create(self, session: AsyncSession, submenu_id: UUID, data: dict) -> RowMapping | None:
        try:
            return await self.repository.create(session=session, submenu_id=submenu_id, **data)
        except IntegrityError:
            raise DishWithThisTitleExists

    async def update(self, session: AsyncSession, submenu_id: UUID, dish_id: UUID, data: dict) -> RowMapping | None:
        try:
            return await self.repository.update(session=session, id=dish_id, submenu_id=submenu_id, data=data)
        except IntegrityError:
            raise DishWithThisTitleExists

    async def delete(self, session: AsyncSession, submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        result = await self.repository.delete(session=session, id=dish_id, submenu_id=submenu_id)
        if result is None:
            raise DishNotFound
        return JSONResponse(status_code=200, content={'detail': 'dish deleted'})
