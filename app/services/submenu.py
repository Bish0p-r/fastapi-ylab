from typing import Sequence
from uuid import UUID

from fastapi.responses import JSONResponse
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import SubMenuNotFound, SubMenuWithThisTitleExists
from app.repositories.submenu import SubMenuRepository


class SubMenuServices:
    def __init__(self, repository: type[SubMenuRepository]):
        self.repository = repository

    async def list(self, session: AsyncSession, menu_id: UUID) -> Sequence[RowMapping]:
        return await self.repository.get_all_with_counts(session=session, menu_id=menu_id)

    async def retrieve(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> RowMapping:
        result = await self.repository.get_one_or_none_with_counts(
            session=session, menu_id=menu_id, submenu_id=submenu_id
        )
        if result is None:
            raise SubMenuNotFound
        return result

    async def create(self, session: AsyncSession, menu_id: UUID, data: dict) -> RowMapping | None:
        try:
            return await self.repository.create(session=session, menu_id=menu_id, **data)
        except IntegrityError:
            raise SubMenuWithThisTitleExists

    async def update(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID, data: dict) -> RowMapping | None:
        try:
            return await self.repository.update(session=session, id=submenu_id, menu_id=menu_id, data=data)
        except IntegrityError:
            raise SubMenuWithThisTitleExists

    async def delete(self, session: AsyncSession, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        result = await self.repository.delete(session=session, id=submenu_id, menu_id=menu_id)
        if result is None:
            raise SubMenuNotFound
        return JSONResponse(status_code=200, content={'detail': 'submenu deleted'})
