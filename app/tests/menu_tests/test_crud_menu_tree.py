from uuid import UUID

from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.tests.utils import reverse


async def test_tree_empty(ac: AsyncClient):
    response = await ac.get(reverse('menu_tree'))

    assert response.status_code == 200
    assert response.json() == []


async def test_tree_menu_create(
    ac: AsyncClient, session: AsyncSession, request: FixtureRequest, menu_repo: MenuRepository
):
    data = {'title': 'Test CRUD menu title', 'description': 'Test CRUD menu description'}
    response = await ac.post(reverse('menu_create'), json=data)
    request.config.option.menu_id = response.json()['id']
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=response.json()['id'])

    assert menu
    assert response.status_code == 201
    assert response.json()['id'] == str(menu.id)
    assert response.json()['title'] == data['title'] == menu.title
    assert response.json()['description'] == data['description'] == menu.description
    assert len(await menu_repo.get_all(session=session)) == 1


async def test_tree_list_with_single_menu(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, menu_repo: MenuRepository
):
    response = await ac.get(reverse('menu_tree'))
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=menu_id)

    assert menu
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]['submenus']) == 0
    assert response.json()[0]['id'] == str(menu.id)
    assert response.json()[0]['title'] == menu.title
    assert response.json()[0]['description'] == menu.description


async def test_tree_submenu_create(
    ac: AsyncClient, session: AsyncSession, request: FixtureRequest, submenu_repo: SubMenuRepository, menu_id: UUID
):
    data = {'title': 'Test CRUD submenu title', 'description': 'Test CRUD submenu description'}
    response = await ac.post(reverse('submenu_create', menu_id=menu_id), json=data)
    request.config.option.submenu_id = response.json()['id']
    submenu = await submenu_repo.get_one_or_none_with_counts(
        session=session, submenu_id=response.json()['id'], menu_id=menu_id
    )

    assert submenu
    assert response.status_code == 201
    assert response.json()['id'] == str(submenu.id)
    assert response.json()['title'] == data['title'] == submenu.title
    assert response.json()['description'] == data['description'] == submenu.description
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 1


async def test_tree_list_with_single_submenu(
    ac: AsyncClient, session: AsyncSession, submenu_id: UUID, submenu_repo: SubMenuRepository, menu_id: UUID
):
    response = await ac.get(reverse('menu_tree'))
    submenu = await submenu_repo.get_one_or_none_with_counts(session=session, submenu_id=submenu_id, menu_id=menu_id)

    assert submenu
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]['submenus']) == 1
    assert response.json()[0]['submenus'][0]['id'] == str(submenu.id)
    assert response.json()[0]['submenus'][0]['title'] == submenu.title
    assert response.json()[0]['submenus'][0]['description'] == submenu.description


async def test_tree_dish_create(
    ac: AsyncClient,
    session: AsyncSession,
    request: FixtureRequest,
    dish_repo: DishRepository,
    menu_id: UUID,
    submenu_id: UUID,
):
    data = {'title': 'Test CRUD submenu title', 'description': 'Test CRUD submenu description', 'price': '100.00'}
    response = await ac.post(reverse('dish_create', menu_id=menu_id, submenu_id=submenu_id), json=data)
    request.config.option.dish_id = response.json()['id']
    dish = await dish_repo.get_one_or_none_dish(
        session=session, dish_id=response.json()['id'], menu_id=menu_id, submenu_id=submenu_id
    )

    assert dish
    assert response.status_code == 201
    assert response.json()['id'] == str(dish.id)
    assert response.json()['title'] == data['title'] == dish.title
    assert response.json()['description'] == data['description'] == dish.description
    assert response.json()['price'] == data['price'] == str(dish.price)
    assert len(await dish_repo.get_all_dishes(session=session, menu_id=menu_id, submenu_id=submenu_id)) == 1


async def test_tree_list(
    ac: AsyncClient,
    session: AsyncSession,
    menu_id: UUID,
    menu_repo: MenuRepository,
    submenu_id: UUID,
    submenu_repo: SubMenuRepository,
    dish_id: UUID,
    dish_repo: DishRepository,
):
    response = await ac.get(reverse('menu_tree'))
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=menu_id)

    assert menu
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(response.json()[0]['submenus']) == 1
    assert len(response.json()[0]['submenus'][0]['dishes']) == 1
    assert response.json()[0]['id'] == str(menu.id)
    assert response.json()[0]['title'] == menu.title
    assert response.json()[0]['description'] == menu.description

    submenu = await submenu_repo.get_one_or_none_with_counts(session=session, submenu_id=submenu_id, menu_id=menu_id)

    assert submenu
    assert response.status_code == 200
    assert response.json()[0]['submenus'][0]['id'] == str(submenu.id)
    assert response.json()[0]['submenus'][0]['title'] == submenu.title
    assert response.json()[0]['submenus'][0]['description'] == submenu.description

    dish = await dish_repo.get_one_or_none_dish(
        session=session, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
    )

    assert dish
    assert response.status_code == 200
    assert response.json()[0]['submenus'][0]['dishes'][0]['id'] == str(dish.id)
    assert response.json()[0]['submenus'][0]['dishes'][0]['title'] == dish.title
    assert response.json()[0]['submenus'][0]['dishes'][0]['description'] == dish.description


async def test_tree_delete_all(
    ac: AsyncClient,
    session: AsyncSession,
    menu_id: UUID,
    menu_repo: MenuRepository,
    submenu_id: UUID,
    submenu_repo: SubMenuRepository,
    dish_id: UUID,
    dish_repo: DishRepository,
):
    response = await ac.delete(reverse('menu_delete', menu_id=menu_id))
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=menu_id)
    submenu = await submenu_repo.get_one_or_none_with_counts(session=session, submenu_id=submenu_id, menu_id=menu_id)
    dish = await dish_repo.get_one_or_none_dish(
        session=session, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
    )

    assert response.status_code == 200
    assert menu is None
    assert submenu is None
    assert dish is None


async def test_tree_list_after_delete(ac: AsyncClient):
    response = await ac.get(reverse('menu_tree'))

    assert response.status_code == 200
    assert response.json() == []
