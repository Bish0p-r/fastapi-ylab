from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.tests import (
    count_dishes,
    count_menus,
    count_submenus,
    is_dish_fields_equal,
    is_menu_fields_equal,
    is_submenu_fields_equal,
)


async def test_counts_menu_create(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Создаю 2 меню и проверяю их количество
    """
    data = {"title": "Test CRUD menu title #1", "description": "Test CRUD menu description #1"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201
    assert await is_menu_fields_equal(response.json()["id"], response.json(), session)
    assert await count_menus(session) == 1

    ids_data["menu_id_1"] = response.json()["id"]
    data = {"title": "Test CRUD menu title #2", "description": "Test CRUD menu description #2"}
    response = await ac.post("api/v1/menus/", json=data)

    assert response.status_code == 201
    assert await is_menu_fields_equal(response.json()["id"], response.json(), session)
    assert await count_menus(session) == 2

    ids_data["menu_id_2"] = response.json()["id"]


async def test_counts_submenu_create(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Создаю 2 подменю для первого меню и 1 подменю для второго меню
    """
    data = {"title": "Test CRUD submenu title #1", "description": "Test CRUD submenu description #1"}
    response = await ac.post(f"api/v1/menus/{ids_data['menu_id_1']}/submenus/", json=data)

    assert response.status_code == 201
    assert await is_submenu_fields_equal(ids_data["menu_id_1"], response.json()["id"], response.json(), session)
    assert await count_submenus(session, menu_id=ids_data["menu_id_1"]) == 1

    ids_data["submenu_id_1"] = response.json()["id"]

    data = {"title": "Test CRUD submenu title #2", "description": "Test CRUD submenu description #2"}
    response = await ac.post(f"api/v1/menus/{ids_data['menu_id_1']}/submenus/", json=data)

    assert response.status_code == 201
    assert await is_submenu_fields_equal(ids_data["menu_id_1"], response.json()["id"], response.json(), session)
    assert await count_submenus(session, menu_id=ids_data["menu_id_1"]) == 2

    ids_data["submenu_id_2"] = response.json()["id"]

    data = {"title": "Test CRUD submenu title #3", "description": "Test CRUD submenu description #3"}
    response = await ac.post(f"api/v1/menus/{ids_data['menu_id_2']}/submenus/", json=data)

    assert response.status_code == 201
    assert await is_submenu_fields_equal(ids_data["menu_id_2"], response.json()["id"], response.json(), session)
    assert await count_submenus(session, menu_id=ids_data["menu_id_2"]) == 1

    ids_data["submenu_id_3"] = response.json()["id"]


async def test_counts_dish_create(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Создаю 2 блюда для первого подменю, 1 блюдо для второго подменю и 1 блюдо для третьего подменю
    """
    data = {"title": "Test CRUD submenu title #1", "description": "Test CRUD submenu description #1", "price": "100.00"}
    response = await ac.post(
        f"api/v1/menus/{ids_data['menu_id_1']}/submenus/{ids_data['submenu_id_1']}/dishes/", json=data
    )

    assert response.status_code == 201
    assert await is_dish_fields_equal(
        ids_data["menu_id_1"], ids_data["submenu_id_1"], response.json()["id"], response.json(), session
    )
    assert await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_1"]) == 1

    ids_data["dish_id_1"] = response.json()["id"]

    data = {"title": "Test CRUD submenu title #2", "description": "Test CRUD submenu description #2", "price": "102.00"}
    response = await ac.post(
        f"api/v1/menus/{ids_data['menu_id_1']}/submenus/{ids_data['submenu_id_1']}/dishes/", json=data
    )

    assert response.status_code == 201
    assert await is_dish_fields_equal(
        ids_data["menu_id_1"], ids_data["submenu_id_1"], response.json()["id"], response.json(), session
    )
    assert await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_1"]) == 2

    ids_data["dish_id_2"] = response.json()["id"]

    data = {"title": "Test CRUD submenu title #3", "description": "Test CRUD submenu description #3", "price": "101.00"}
    response = await ac.post(
        f"api/v1/menus/{ids_data['menu_id_1']}/submenus/{ids_data['submenu_id_2']}/dishes/", json=data
    )

    assert response.status_code == 201
    assert await is_dish_fields_equal(
        ids_data["menu_id_1"], ids_data["submenu_id_2"], response.json()["id"], response.json(), session
    )
    assert await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_2"]) == 1

    ids_data["dish_id_3"] = response.json()["id"]

    data = {"title": "Test CRUD submenu title #4", "description": "Test CRUD submenu description #4", "price": "10.00"}
    response = await ac.post(
        f"api/v1/menus/{ids_data['menu_id_2']}/submenus/{ids_data['submenu_id_3']}/dishes/", json=data
    )

    assert response.status_code == 201
    assert await is_dish_fields_equal(
        ids_data["menu_id_2"], ids_data["submenu_id_3"], response.json()["id"], response.json(), session
    )
    assert await count_dishes(session, menu_id=ids_data["menu_id_2"], submenu_id=ids_data["submenu_id_3"]) == 1

    ids_data["dish_id_4"] = response.json()["id"]


async def test_counts(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Проверяю количество подменю и блюд в меню
    """
    response = await ac.get(f"api/v1/menus/{ids_data['menu_id_1']}")

    assert response.status_code == 200
    assert response.json()["id"] == ids_data["menu_id_1"]

    submenus_count = await count_submenus(session, menu_id=ids_data["menu_id_1"])
    dishes_count = await count_dishes(
        session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_1"]
    ) + await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_2"])

    assert response.json()["submenus_count"] == submenus_count == 2
    assert response.json()["dishes_count"] == dishes_count == 3

    response = await ac.get(f"api/v1/menus/{ids_data['menu_id_2']}")

    assert response.status_code == 200
    assert response.json()["id"] == ids_data["menu_id_2"]

    submenus_count = await count_submenus(session, menu_id=ids_data["menu_id_2"])
    dishes_count = await count_dishes(session, menu_id=ids_data["menu_id_2"], submenu_id=ids_data["submenu_id_3"])

    assert response.json()["submenus_count"] == submenus_count == 1
    assert response.json()["dishes_count"] == dishes_count == 1


async def test_counts_submenu_delete(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Удаляю первое подменю и проверяю количество подменю и блюд в первом меню
    """
    response = await ac.delete(f"api/v1/menus/{ids_data['menu_id_1']}/submenus/{ids_data['submenu_id_1']}")

    assert response.status_code == 200
    assert await count_submenus(session, menu_id=ids_data["menu_id_1"]) == 1
    assert await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_1"]) == 0


async def test_counts_after_delete(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Проверяю количество подменю и блюд в меню после удаления первого подменю
    """
    response = await ac.get(f"api/v1/menus/{ids_data['menu_id_1']}")

    assert response.status_code == 200
    assert response.json()["id"] == ids_data["menu_id_1"]

    submenus_count = await count_submenus(session, menu_id=ids_data["menu_id_1"])
    dishes_count = await count_dishes(
        session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_1"]
    ) + await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_2"])

    assert response.json()["submenus_count"] == submenus_count == 1
    assert response.json()["dishes_count"] == dishes_count == 1

    response = await ac.get(f"api/v1/menus/{ids_data['menu_id_2']}")

    assert response.status_code == 200
    assert response.json()["id"] == ids_data["menu_id_2"]

    submenus_count = await count_submenus(session, menu_id=ids_data["menu_id_2"])
    dishes_count = await count_dishes(session, menu_id=ids_data["menu_id_2"], submenu_id=ids_data["submenu_id_3"])

    assert response.json()["submenus_count"] == submenus_count == 1
    assert response.json()["dishes_count"] == dishes_count == 1


async def test_counts_submenu_delete_all(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Удаляю все подменю и проверяю количество подменю и блюд
    """
    response = await ac.delete(f"api/v1/menus/{ids_data['menu_id_1']}/submenus/{ids_data['submenu_id_2']}")

    assert response.status_code == 200
    assert await count_submenus(session, menu_id=ids_data["menu_id_1"]) == 0
    assert await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_2"]) == 0

    response = await ac.delete(f"api/v1/menus/{ids_data['menu_id_2']}/submenus/{ids_data['submenu_id_3']}")

    assert response.status_code == 200
    assert await count_submenus(session, menu_id=ids_data["menu_id_2"]) == 0
    assert await count_dishes(session, menu_id=ids_data["menu_id_2"], submenu_id=ids_data["submenu_id_3"]) == 0


async def test_counts_after_delete_all(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Проверяю количество подменю и блюд в меню после удаления всех подменю
    """
    response = await ac.get(f"api/v1/menus/{ids_data['menu_id_1']}")

    assert response.status_code == 200
    assert response.json()["id"] == ids_data["menu_id_1"]

    submenus_count = await count_submenus(session, menu_id=ids_data["menu_id_1"])
    dishes_count = await count_dishes(
        session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_1"]
    ) + await count_dishes(session, menu_id=ids_data["menu_id_1"], submenu_id=ids_data["submenu_id_2"])

    assert response.json()["submenus_count"] == submenus_count == 0
    assert response.json()["dishes_count"] == dishes_count == 0

    response = await ac.get(f"api/v1/menus/{ids_data['menu_id_2']}")

    assert response.status_code == 200
    assert response.json()["id"] == ids_data["menu_id_2"]

    submenus_count = await count_submenus(session, menu_id=ids_data["menu_id_2"])
    dishes_count = await count_dishes(session, menu_id=ids_data["menu_id_2"], submenu_id=ids_data["submenu_id_3"])

    assert response.json()["submenus_count"] == submenus_count == 0
    assert response.json()["dishes_count"] == dishes_count == 0


async def test_counts_delete_all_menus(ac: AsyncClient, session: AsyncSession, ids_data: dict):
    """
    Удаляю все меню
    """
    response = await ac.delete(f"api/v1/menus/{ids_data['menu_id_1']}")

    assert response.status_code == 200
    assert await count_menus(session) == 1

    response = await ac.delete(f"api/v1/menus/{ids_data['menu_id_2']}")

    assert response.status_code == 200
    assert await count_menus(session) == 0
