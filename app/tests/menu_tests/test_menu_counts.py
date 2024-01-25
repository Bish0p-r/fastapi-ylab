from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest


async def test_counts_menu_create(ac: AsyncClient, request: FixtureRequest):
    data = {"title": "Test title", "description": "Test description"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201

    request.config.option.menu_id = response.json()["id"]


async def test_counts_submenu_create(ac: AsyncClient, menu_id: UUID, request: FixtureRequest):
    data = {"title": "Test title", "description": "Test description"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/", json=data)

    assert response.status_code == 201

    request.config.option.submenu_id = response.json()["id"]


async def test_counts_dishes_create(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    data = {"title": "Test title #1", "description": "Test description #1", "price": "0.01"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", json=data)

    assert response.status_code == 201

    data = {"title": "Test title #2", "description": "Test description #2", "price": "0.02"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", json=data)

    assert response.status_code == 201


async def test_counts_menu_retrieve(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()["submenus_count"] == 1
    assert response.json()["dishes_count"] == 2


async def test_submenu_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["dishes_count"] == 2


async def test_counts_submenu_delete(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200


async def test_counts_submenu_deleted_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/")

    assert response.status_code == 200
    assert response.json() == []


async def test_counts_dishes_deleted_list(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")

    assert response.status_code == 200
    assert response.json() == []


async def test_counts_menu_deleted_retrieve(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()["submenus_count"] == 0
    assert response.json()["dishes_count"] == 0


async def test_counts_menu_delete(ac: AsyncClient, menu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200


async def test_counts_menu_deleted_list(ac: AsyncClient):
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    assert response.json() == []
