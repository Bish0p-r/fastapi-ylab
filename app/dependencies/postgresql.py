from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql import async_session_maker


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


GetSession = Annotated[AsyncSession, Depends(get_async_session)]
