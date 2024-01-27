from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.tests import (
    count_dishes,
    count_menus,
    count_submenus,
    is_dish_fields_equal,
    is_menu_fields_equal,
    is_submenu_fields_equal,
)


async def test_dish_menu_create(ac: AsyncClient, request: FixtureRequest, session: AsyncSession):
    data = {"title": "Test CRUD menu title", "description": "Test CRUD menu description"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201

    request.config.option.menu_id = response.json()["id"]
    assert await is_menu_fields_equal(response.json()["id"], response.json(), session)
    assert await count_menus(session) == 1


async def test_dish_submenu_create(ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_id: UUID):
    data = {"title": "Test CRUD submenu title", "description": "Test CRUD submenu description"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/", json=data)

    assert response.status_code == 201

    request.config.option.submenu_id = response.json()["id"]

    assert await is_submenu_fields_equal(menu_id, response.json()["id"], response.json(), session)
    assert await count_submenus(session, menu_id=menu_id) == 1


async def test_dish_empty_list(ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")

    assert response.status_code == 200
    assert len(response.json()) == await count_dishes(session, menu_id=menu_id, submenu_id=submenu_id) == 0


async def test_dish_create(
    ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_id: UUID, submenu_id: UUID
):
    data = {"title": "Test CRUD submenu title", "description": "Test CRUD submenu description", "price": "100.00"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", json=data)

    assert response.status_code == 201

    request.config.option.dish_id = response.json()["id"]

    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]
    assert await is_dish_fields_equal(menu_id, submenu_id, response.json()["id"], response.json(), session)
    assert await count_dishes(session, menu_id=menu_id, submenu_id=submenu_id) == 1


async def test_dish_list(ac: AsyncClient, session: AsyncSession, submenu_id: UUID, menu_id: UUID, dish_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")

    assert response.status_code == 200
    assert len(response.json()) == await count_dishes(session, menu_id=menu_id, submenu_id=submenu_id)


async def test_dish_retrieve(ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 200
    assert await is_dish_fields_equal(menu_id, submenu_id, dish_id, response.json(), session)


async def test_dish_update(ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    data = {"title": "Updated test CRUD title", "description": "Updated test CRUD description", "price": "200.00"}
    response = await ac.patch(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]
    assert await is_dish_fields_equal(menu_id, submenu_id, dish_id, response.json(), session)


async def test_dish_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 200
    assert await count_dishes(session, menu_id=menu_id, submenu_id=submenu_id) == 0


async def test_submenu_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert await count_submenus(session, menu_id=menu_id) == 0


async def test_menu_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert await count_menus(session) == 0
