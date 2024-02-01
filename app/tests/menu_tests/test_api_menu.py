from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest

from app.tests.utils import reverse


async def test_menu_empty_list(ac: AsyncClient):
    response = await ac.get(reverse('menu_list'))

    assert response.status_code == 200
    assert response.json() == []


async def test_menu_create(ac: AsyncClient, request: FixtureRequest):
    data = {'title': 'Test title', 'description': 'Test description'}
    response = await ac.post(reverse('menu_create'), json=data)

    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']

    request.config.option.menu_id = response.json()['id']


async def test_menu_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(reverse('menu_list'))

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == menu_id


async def test_menu_retrieve(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(reverse('menu_retrieve', menu_id=menu_id))

    assert response.status_code == 200
    assert response.json()['id'] == menu_id
    assert response.json()['title'] == 'Test title'
    assert response.json()['description'] == 'Test description'


async def test_menu_update(ac: AsyncClient, menu_id: UUID):
    data = {'title': 'Updated test title', 'description': 'Updated test description'}
    response = await ac.patch(reverse('menu_update', menu_id=menu_id), json=data)

    assert response.status_code == 200
    assert response.json()['id'] == menu_id
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']


async def test_updated_menu_retrieve(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(reverse('menu_retrieve', menu_id=menu_id))

    assert response.status_code == 200
    assert response.json()['id'] == menu_id
    assert response.json()['title'] == 'Updated test title', 'description'
    assert response.json()['description'] == 'Updated test description'


async def test_menu_delete(ac: AsyncClient, menu_id: UUID):
    response = await ac.delete(reverse('menu_delete', menu_id=menu_id))

    assert response.status_code == 200


async def test_deleted_menu_list(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(reverse('menu_list'))

    assert response.status_code == 200
    assert response.json() == []


async def test_menu_retrieve_deleted(ac: AsyncClient, menu_id: UUID):
    response = await ac.get(reverse('menu_retrieve', menu_id=menu_id))

    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
