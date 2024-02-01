from uuid import UUID

from httpx import AsyncClient
from pytest import FixtureRequest

from app.tests.utils import reverse


async def test_dish_menu_create(ac: AsyncClient, request: FixtureRequest):
    data = {'title': 'Test title', 'description': 'Test description'}
    response = await ac.post(reverse('menu_create'), json=data)

    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']

    request.config.option.menu_id = response.json()['id']


async def test_dish_submenu_create(ac: AsyncClient, menu_id: UUID, request: FixtureRequest):
    data = {'title': 'Test title', 'description': 'Test description'}
    response = await ac.post(reverse('submenu_create', menu_id=menu_id), json=data)

    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']

    request.config.option.submenu_id = response.json()['id']


async def test_dish_empty_list(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(reverse('dish_list', menu_id=menu_id, submenu_id=submenu_id))

    assert response.status_code == 200
    assert response.json() == []


async def test_dish_create(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, request: FixtureRequest):
    data = {'title': 'Test title', 'description': 'Test description', 'price': '0.01'}
    response = await ac.post(reverse('dish_create', menu_id=menu_id, submenu_id=submenu_id), json=data)

    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']
    assert response.json()['price'] == data['price']

    request.config.option.dish_id = response.json()['id']


async def test_dish_list(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(reverse('dish_list', menu_id=menu_id, submenu_id=submenu_id))

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_dish_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    response = await ac.get(reverse('dish_retrieve', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))

    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == 'Test title'
    assert response.json()['description'] == 'Test description'
    assert response.json()['price'] == '0.01'


async def test_dish_update(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    data = {'title': 'Updated test title', 'description': 'Updated test description', 'price': '10.01'}
    url = reverse('dish_update', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    response = await ac.patch(url, json=data)

    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == data['title']
    assert response.json()['description'] == data['description']
    assert response.json()['price'] == data['price']


async def test_dish_updated_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    response = await ac.get(reverse('dish_retrieve', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))

    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == 'Updated test title', 'description'
    assert response.json()['description'] == 'Updated test description'
    assert response.json()['price'] == '10.01'


async def test_dish_delete(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    response = await ac.delete(reverse('dish_delete', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))

    assert response.status_code == 200


async def test_dish_deleted_list(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(reverse('dish_list', menu_id=menu_id, submenu_id=submenu_id))

    assert response.status_code == 200
    assert response.json() == []


async def test_dish_deleted_retrieve(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    response = await ac.get(reverse('dish_retrieve', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))

    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


async def test_dish_submenu_delete(ac: AsyncClient, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    response = await ac.delete(reverse('submenu_delete', menu_id=menu_id, submenu_id=submenu_id))

    assert response.status_code == 200


async def test_dish_submenu_deleted_list(ac: AsyncClient, menu_id: UUID, submenu_id: UUID):
    response = await ac.get(reverse('dish_list', menu_id=menu_id, submenu_id=submenu_id))

    assert response.status_code == 200
    assert response.json() == []


async def test_dish_menu_delete(ac: AsyncClient, menu_id: UUID):
    response = await ac.delete(reverse('menu_delete', menu_id=menu_id))

    assert response.status_code == 200


async def test_dish_menu_deleted_list(ac: AsyncClient):
    response = await ac.get(reverse('menu_list'))

    assert response.status_code == 200
    assert response.json() == []
