from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_scoped_session

from app.db.postgresql import async_session_maker


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        async_session_maker,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as session:
            yield session
    finally:
        await scoped_factory.remove()
