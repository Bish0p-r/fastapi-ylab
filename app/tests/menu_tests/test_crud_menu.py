from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.menu import MenuRepository
from app.schemas.menu import MenuWithCountsSchema
from app.tests.utils import reverse


async def test_menu_empty_list(ac: AsyncClient, session: AsyncSession, menu_repo: MenuRepository):
    response = await ac.get(reverse('menu_list'))

    assert response.status_code == 200
    assert len(await menu_repo.get_all(session=session)) == 0


async def test_menu_create(ac: AsyncClient, request: FixtureRequest, session: AsyncSession, menu_repo: MenuRepository):
    data = {'title': 'Test CRUD title', 'description': 'Test CRUD description'}
    response = await ac.post(reverse('menu_list'), json=data)
    request.config.option.menu_id = response.json()['id']
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=response.json()['id'])

    assert menu
    assert response.status_code == 201
    assert response.json()['id'] == str(menu.id)
    assert response.json()['title'] == data['title'] == menu.title
    assert response.json()['description'] == data['description'] == menu.description
    assert len(await menu_repo.get_all(session=session)) == 1


async def test_menu_invalid_create(ac: AsyncClient, session: AsyncSession, menu_repo: MenuRepository):
    data = {'title': 'Test CRUD title', 'description': 'Test CRUD description'}
    response = await ac.post(reverse('menu_create'), json=data)

    assert response.status_code == 409
    assert len(await menu_repo.get_all(session=session)) == 1


async def test_menu_list(
    ac: AsyncClient, session: AsyncSession, menu_id: UUID, menu_obj: MenuWithCountsSchema, menu_repo: MenuRepository
):
    response = await ac.get(reverse('menu_list'))

    assert response.status_code == 200
    assert len(response.json()) == len(await menu_repo.get_all(session=session))
    assert response.json()[0]['id'] == str(menu_id)
    assert response.json()[0]['title'] == menu_obj.title
    assert response.json()[0]['description'] == menu_obj.description


async def test_menu_retrieve(ac: AsyncClient, session: AsyncSession, menu_obj: MenuWithCountsSchema):
    response = await ac.get(reverse('menu_retrieve', menu_id=menu_obj.id))

    assert response.status_code == 200
    assert response.json()['id'] == str(menu_obj.id)
    assert response.json()['title'] == menu_obj.title
    assert response.json()['description'] == menu_obj.description
    assert response.json()['submenus_count'] == menu_obj.submenus_count == 0
    assert response.json()['dishes_count'] == menu_obj.dishes_count == 0


async def test_menu_update(ac: AsyncClient, session: AsyncSession, menu_id: UUID, menu_repo: MenuRepository):
    data = {'title': 'Updated test CRUD title', 'description': 'Updated test CRUD description'}
    response = await ac.patch(reverse('menu_update', menu_id=menu_id), json=data)
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=menu_id)

    assert menu
    assert response.status_code == 200
    assert response.json()['id'] == str(menu.id)
    assert response.json()['title'] == menu.title
    assert response.json()['description'] == menu.description == data['description']


async def test_menu_delete(ac: AsyncClient, session: AsyncSession, menu_id: UUID, menu_repo: MenuRepository):
    response = await ac.delete(reverse('menu_update', menu_id=menu_id))

    assert response.status_code == 200
    assert len(await menu_repo.get_all(session=session)) == 0
