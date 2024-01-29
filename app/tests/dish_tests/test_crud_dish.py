from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.repositories.dish import DishRepository
from app.schemas.dish import DishSchema


async def test_dish_menu_create(
        ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_repo: MenuRepository
):
    data = {"title": "Test CRUD menu title", "description": "Test CRUD menu description"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201

    request.config.option.menu_id = response.json()["id"]
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=response.json()["id"])

    assert menu
    assert response.json()["id"] == str(menu.id)
    assert response.json()["title"] == data["title"] == menu.title
    assert response.json()["description"] == data["description"] == menu.description
    assert len(await menu_repo.get_all(session=session)) == 1


async def test_dish_submenu_create(
        ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_id: UUID, submenu_repo: SubMenuRepository
):
    data = {"title": "Test CRUD submenu title", "description": "Test CRUD submenu description"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/", json=data)

    assert response.status_code == 201

    request.config.option.submenu_id = response.json()["id"]
    submenu = await submenu_repo.get_one_or_none_with_counts(
        session=session, submenu_id=response.json()["id"], menu_id=menu_id
    )

    assert submenu
    assert response.json()["id"] == str(submenu.id)
    assert response.json()["title"] == data["title"] == submenu.title
    assert response.json()["description"] == data["description"] == submenu.description
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 1


async def test_dish_empty_list(
        ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_repo: DishRepository
):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")

    assert response.status_code == 200
    assert response.json() == []
    assert len(await dish_repo.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id)) == 0


async def test_dish_create(
    ac: AsyncClient,
    request: FixtureRequest,
    session: AsyncSession,
    menu_id: UUID,
    submenu_id: UUID,
    dish_repo: DishRepository
):
    data = {"title": "Test CRUD submenu title", "description": "Test CRUD submenu description", "price": "100.00"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", json=data)

    assert response.status_code == 201

    request.config.option.dish_id = response.json()["id"]
    dish = await dish_repo.get_one_or_none(
        session=session, dish_id=response.json()["id"], menu_id=menu_id, submenu_id=submenu_id
    )

    assert dish
    assert response.json()["id"] == str(dish.id)
    assert response.json()["title"] == data["title"] == dish.title
    assert response.json()["description"] == data["description"] == dish.description
    assert response.json()["price"] == data["price"] == str(dish.price)
    assert len(await dish_repo.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id)) == 1


async def test_dish_invalid_create(
        ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_repo: DishRepository
):
    data = {"title": "Test CRUD submenu title", "description": "Test CRUD submenu description", "price": "100.00"}
    response = await ac.post(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", json=data)

    assert response.status_code == 400
    assert len(await dish_repo.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id)) == 1


async def test_dish_list(
        ac: AsyncClient,
        session: AsyncSession,
        submenu_id: UUID,
        menu_id: UUID,
        dish_id: UUID,
        dish_repo: DishRepository
):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(await dish_repo.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id)) == 1


async def test_dish_retrieve(
        ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, dish_obj: DishSchema
):
    response = await ac.get(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_obj.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(dish_obj.id)
    assert response.json()["title"] == dish_obj.title
    assert response.json()["description"] == dish_obj.description
    assert response.json()["price"] == str(dish_obj.price)


async def test_dish_update(
        ac: AsyncClient,
        session: AsyncSession,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_repo: DishRepository
):
    data = {"title": "Updated test CRUD title", "description": "Updated test CRUD description", "price": "200.00"}
    response = await ac.patch(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=data)
    dish = await dish_repo.get_one_or_none(session=session, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)

    assert dish
    assert response.status_code == 200
    assert response.json()["title"] == data["title"] == dish.title
    assert response.json()["description"] == data["description"] == dish.description
    assert response.json()["price"] == data["price"] == str(dish.price)


async def test_dish_delete(
        ac: AsyncClient,
        session: AsyncSession,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_repo: DishRepository
):
    response = await ac.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 200
    assert len(await dish_repo.get_all(session=session, menu_id=menu_id, submenu_id=submenu_id)) == 0


async def test_submenu_delete(
        ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, submenu_repo: SubMenuRepository
):
    response = await ac.delete(f"api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 0


async def test_menu_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID, menu_repo: MenuRepository):
    response = await ac.delete(f"api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert len(await menu_repo.get_all(session=session)) == 0
