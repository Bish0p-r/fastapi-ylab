import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.postgresql import Base, async_engine
from app.main import app as fastapi_app
from app.db.postgresql import async_session_maker


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest.fixture
def menu_id(request):
    return request.config.getoption("menu_id")


@pytest.fixture
def submenu_id(request):
    return request.config.getoption("submenu_id")


@pytest.fixture
def dish_id(request):
    return request.config.getoption("dish_id")


@pytest.fixture(scope="session")
def ids_data():
    data = {}
    yield data
