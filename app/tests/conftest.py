import asyncio
from uuid import UUID

import pytest
from cashews import cache
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.postgresql import Base, async_engine, async_session_maker
from app.main import app as fastapi_app
from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.schemas.dish import DishSchema
from app.schemas.menu import MenuWithCountsSchema
from app.schemas.submenu import SubMenuWithCountSchema


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
def init_cache():
    cache.setup(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function')
async def session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def menu_id(request):
    return request.config.getoption('menu_id')


@pytest.fixture
async def submenu_id(request):
    return request.config.getoption('submenu_id')


@pytest.fixture
async def dish_id(request):
    return request.config.getoption('dish_id')


@pytest.fixture(scope='session')
async def ids_data():
    data = {}
    yield data


@pytest.fixture(scope='function')
async def menu_obj(menu_id: UUID, session: AsyncSession) -> MenuWithCountsSchema:
    return await MenuRepository.get_one_or_none_with_counts(session=session, menu_id=menu_id)


@pytest.fixture(scope='function')
async def submenu_obj(menu_id: UUID, submenu_id: UUID, session: AsyncSession) -> SubMenuWithCountSchema:
    return await SubMenuRepository.get_one_or_none_with_counts(session=session, submenu_id=submenu_id, menu_id=menu_id)


@pytest.fixture(scope='function')
async def dish_obj(menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession) -> DishSchema:
    return await DishRepository.get_one_or_none_dish(
        session=session, submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id
    )


@pytest.fixture
async def menu_repo(session: AsyncSession) -> type[MenuRepository]:
    return MenuRepository


@pytest.fixture
async def submenu_repo(session: AsyncSession) -> type[SubMenuRepository]:
    return SubMenuRepository


@pytest.fixture
async def dish_repo(session: AsyncSession) -> type[DishRepository]:
    return DishRepository
