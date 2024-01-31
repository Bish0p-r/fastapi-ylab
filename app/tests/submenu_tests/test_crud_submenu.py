from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.schemas.submenu import SubMenuWithCountSchema
from app.tests.utils import reverse


async def test_submenu_menu_create(
    ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_repo: MenuRepository
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


async def test_submenu_empty_list(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_repo: SubMenuRepository
):
    response = await ac.get(reverse('submenu_list', menu_id=menu_id))

    assert response.status_code == 200
    assert response.json() == []
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 0


async def test_submenu_create(
    ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_id: UUID, submenu_repo: SubMenuRepository
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


async def test_submenu_invalid_create(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_repo: SubMenuRepository
):
    data = {'title': 'Test CRUD submenu title', 'description': 'Test CRUD submenu description'}
    response = await ac.post(reverse('submenu_create', menu_id=menu_id), json=data)

    assert response.status_code == 400
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 1


async def test_submenu_list(
    ac: AsyncClient, session: AsyncSession, submenu_id: UUID, menu_id: UUID, submenu_repo: SubMenuRepository
):
    response = await ac.get(reverse('submenu_list', menu_id=menu_id))

    assert response.status_code == 200
    assert len(response.json()) == len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id))


async def test_submenu_retrieve(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_obj: SubMenuWithCountSchema
):
    response = await ac.get(reverse('submenu_retrieve', menu_id=menu_id, submenu_id=submenu_obj.id))

    assert response.status_code == 200
    assert response.json()['id'] == str(submenu_obj.id)
    assert response.json()['title'] == submenu_obj.title
    assert response.json()['description'] == submenu_obj.description
    assert response.json()['dishes_count'] == submenu_obj.dishes_count == 0


async def test_submenu_update(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, submenu_repo: SubMenuRepository
):
    data = {'title': 'Updated test CRUD title', 'description': 'Updated test CRUD description'}
    response = await ac.patch(reverse('submenu_update', menu_id=menu_id, submenu_id=submenu_id), json=data)
    submenu = await submenu_repo.get_one_or_none_with_counts(
        session=session, submenu_id=response.json()['id'], menu_id=menu_id
    )

    assert submenu
    assert response.status_code == 200
    assert response.json()['id'] == str(submenu.id)
    assert response.json()['title'] == data['title'] == submenu.title
    assert response.json()['description'] == data['description'] == submenu.description
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 1


async def test_submenu_delete(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, submenu_id: UUID, submenu_repo: SubMenuRepository
):
    response = await ac.delete(reverse('submenu_delete', menu_id=menu_id, submenu_id=submenu_id))

    assert response.status_code == 200
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=menu_id)) == 0


async def test_menu_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID, menu_repo: MenuRepository):
    response = await ac.delete(reverse('menu_update', menu_id=menu_id))

    assert response.status_code == 200
    assert len(await menu_repo.get_all(session=session)) == 0
