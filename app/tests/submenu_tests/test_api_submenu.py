from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest


async def test_menu_create(ac: AsyncClient, request: FixtureRequest):
    data = {"title": "Test title", "description": "Test description"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]

    request.config.option.menu_id = response.json()["id"]


async def test_submenu_empty_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/")

    assert response.status_code == 200
    assert response.json() == []


async def test_submenu_create(ac: AsyncClient, menu_id: UUID, request: FixtureRequest):
    data = {"title": "Test title", "description": "Test description"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/", json=data)

    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]

    request.config.option.submenu_id = response.json()["id"]


async def test_submenu_list(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == submenu_id


async def test_submenu_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == "Test title"
    assert response.json()["description"] == "Test description"


async def test_submenu_update(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    data = {"title": "Updated test title", "description": "Updated test description"}
    response = await ac.patch(f"api/v1/menus/{menu_id}/submenus/{submenu_id}", json=data)

    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]


async def test_submenu_updated_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == "Updated test title", "description"
    assert response.json()["description"] == "Updated test description"


async def test_submenu_delete(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200


async def test_submenu_deleted_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/")

    assert response.status_code == 200
    assert response.json() == []


async def test_submenu_deleted_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


async def test_submenu_delete_menu(ac: AsyncClient, menu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200


async def test_submenu_deleted_menu_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    assert response.json() == []
