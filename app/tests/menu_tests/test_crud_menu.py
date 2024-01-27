from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.tests import is_menu_fields_equal, count_menus


async def test_menu_empty_list(ac: AsyncClient, session: AsyncSession):
    response = await ac.get(f"api/v1/menus/")

    assert response.status_code == 200
    assert len(response.json()) == await count_menus(session) == 0


async def test_menu_create(ac: AsyncClient, request: FixtureRequest, session: AsyncSession):
    data = {"title": "Test CRUD title", "description": "Test CRUD description"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201

    request.config.option.menu_id = response.json()["id"]

    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert await is_menu_fields_equal(response.json()["id"], response.json(), session)
    assert await count_menus(session) == 1


async def test_menu_list(ac: AsyncClient, session: AsyncSession, menu_id: UUID):
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    assert len(response.json()) == await count_menus(session)
    assert await is_menu_fields_equal(menu_id, response.json()[0], session)


async def test_menu_retrieve(ac: AsyncClient, session: AsyncSession, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200

    assert await is_menu_fields_equal(menu_id, response.json(), session)


async def test_menu_update(ac: AsyncClient, session: AsyncSession, menu_id: UUID):
    data = {"title": "Updated test CRUD title", "description": "Updated test CRUD description"}
    response = await ac.patch(f"api/v1/menus/{menu_id}", json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert await is_menu_fields_equal(menu_id, response.json(), session)


async def test_menu_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200

    assert await count_menus(session) == 0

