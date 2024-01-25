from uuid import UUID

from pytest import FixtureRequest
from httpx import AsyncClient


async def test_menu_empty_list(ac: AsyncClient):
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    assert response.json() == []


async def test_menu_create(ac: AsyncClient, request: FixtureRequest):
    data = {"title": "Test title", "description": "Test description"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]

    request.config.option.menu_id = response.json()["id"]


async def test_menu_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == menu_id


async def test_menu_retrieve(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == "Test title"
    assert response.json()["description"] == "Test description"


async def test_menu_update(ac: AsyncClient, menu_id: UUID):
    data = {"title": "Updated test title", "description": "Updated test description"}
    response = await ac.patch(f"api/v1/menus/{menu_id}", json=data)

    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]


async def test_updated_menu_retrieve(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == "Updated test title", "description"
    assert response.json()["description"] == "Updated test description"


async def test_menu_delete(ac: AsyncClient, menu_id: UUID):
    response = await ac.delete(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200


async def test_deleted_menu_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    assert response.json() == []


async def test_menu_retrieve_deleted(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(f"api/v1/menus/{menu_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
