from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubMenuRepository
from app.tests.utils import reverse


async def test_counts_2_menus_create(ac: AsyncClient, session: AsyncSession, ids_data: dict, menu_repo: MenuRepository):
    """Создаю 2 меню и проверяю их количество в бд"""
    data = {'title': 'Test CRUD menu title #1', 'description': 'Test CRUD menu description #1'}
    response = await ac.post(reverse('menu_create'), json=data)
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=response.json()['id'])

    assert menu
    assert response.status_code == 201
    assert response.json()['id'] == str(menu.id)
    assert response.json()['title'] == data['title'] == menu.title
    assert response.json()['description'] == data['description'] == menu.description
    assert len(await menu_repo.get_all(session=session)) == 1

    ids_data['menu_id_1'] = response.json()['id']
    data = {'title': 'Test CRUD menu title #2', 'description': 'Test CRUD menu description #2'}
    response = await ac.post(reverse('menu_create'), json=data)
    menu = await menu_repo.get_one_or_none_with_counts(session=session, menu_id=response.json()['id'])

    assert menu
    assert response.status_code == 201
    assert response.json()['id'] == str(menu.id)
    assert response.json()['title'] == data['title'] == menu.title
    assert response.json()['description'] == data['description'] == menu.description
    assert len(await menu_repo.get_all(session=session)) == 2

    ids_data['menu_id_2'] = response.json()['id']


async def test_counts_3_submenus_create(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, submenu_repo: SubMenuRepository
):
    """Создаю 2 подменю для первого меню и 1 подменю для второго меню"""
    data = {'title': 'Test CRUD submenu title #1', 'description': 'Test CRUD submenu description #1'}
    response = await ac.post(reverse('submenu_create', menu_id=ids_data['menu_id_1']), json=data)
    submenu = await submenu_repo.get_one_or_none_with_counts(
        session=session, submenu_id=response.json()['id'], menu_id=ids_data['menu_id_1']
    )

    assert submenu
    assert response.status_code == 201
    assert response.json()['id'] == str(submenu.id)
    assert response.json()['title'] == data['title'] == submenu.title
    assert response.json()['description'] == data['description'] == submenu.description
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=ids_data['menu_id_1'])) == 1

    ids_data['submenu_id_1'] = response.json()['id']

    data = {'title': 'Test CRUD submenu title #2', 'description': 'Test CRUD submenu description #2'}
    response = await ac.post(reverse('submenu_create', menu_id=ids_data['menu_id_1']), json=data)
    submenu = await submenu_repo.get_one_or_none_with_counts(
        session=session, submenu_id=response.json()['id'], menu_id=ids_data['menu_id_1']
    )

    assert submenu
    assert response.status_code == 201
    assert response.json()['id'] == str(submenu.id)
    assert response.json()['title'] == data['title'] == submenu.title
    assert response.json()['description'] == data['description'] == submenu.description
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=ids_data['menu_id_1'])) == 2

    ids_data['submenu_id_2'] = response.json()['id']

    data = {'title': 'Test CRUD submenu title #3', 'description': 'Test CRUD submenu description #3'}
    response = await ac.post(reverse('submenu_create', menu_id=ids_data['menu_id_2']), json=data)
    submenu = await submenu_repo.get_one_or_none_with_counts(
        session=session, submenu_id=response.json()['id'], menu_id=ids_data['menu_id_2']
    )

    assert submenu
    assert response.status_code == 201
    assert response.json()['id'] == str(submenu.id)
    assert response.json()['title'] == data['title'] == submenu.title
    assert response.json()['description'] == data['description'] == submenu.description
    assert len(await submenu_repo.get_all_with_counts(session=session, menu_id=ids_data['menu_id_2'])) == 1

    ids_data['submenu_id_3'] = response.json()['id']


async def test_counts_4_dishes_create(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, dish_repo: DishRepository
):
    """Создаю 2 блюда для первого подменю, 1 блюдо для второго подменю и 1 блюдо для третьего подменю"""
    data = {'title': 'Test CRUD submenu title #1', 'description': 'Test CRUD submenu description #1', 'price': '100.00'}
    response = await ac.post(
        reverse('dish_create', menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1']), json=data
    )
    dish = await dish_repo.get_one_or_none_dish(
        session=session,
        dish_id=response.json()['id'],
        menu_id=ids_data['menu_id_1'],
        submenu_id=ids_data['submenu_id_1'],
    )
    dish_count = len(
        await dish_repo.get_all_dishes(
            session=session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1']
        )
    )

    assert dish
    assert response.status_code == 201
    assert response.json()['id'] == str(dish.id)
    assert response.json()['title'] == data['title'] == dish.title
    assert response.json()['description'] == data['description'] == dish.description
    assert response.json()['price'] == data['price'] == str(dish.price)
    assert dish_count == 1

    ids_data['dish_id_1'] = response.json()['id']

    data = {'title': 'Test CRUD submenu title #2', 'description': 'Test CRUD submenu description #2', 'price': '102.00'}
    response = await ac.post(
        reverse('dish_create', menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1']), json=data
    )
    dish = await dish_repo.get_one_or_none_dish(
        session=session,
        dish_id=response.json()['id'],
        menu_id=ids_data['menu_id_1'],
        submenu_id=ids_data['submenu_id_1'],
    )
    dish_count = len(
        await dish_repo.get_all_dishes(
            session=session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1']
        )
    )

    assert dish
    assert response.status_code == 201
    assert response.json()['id'] == str(dish.id)
    assert response.json()['title'] == data['title'] == dish.title
    assert response.json()['description'] == data['description'] == dish.description
    assert response.json()['price'] == data['price'] == str(dish.price)
    assert dish_count == 2

    ids_data['dish_id_2'] = response.json()['id']

    data = {'title': 'Test CRUD submenu title #3', 'description': 'Test CRUD submenu description #3', 'price': '101.00'}
    response = await ac.post(
        reverse('dish_create', menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2']), json=data
    )
    dish = await dish_repo.get_one_or_none_dish(
        session=session,
        dish_id=response.json()['id'],
        menu_id=ids_data['menu_id_1'],
        submenu_id=ids_data['submenu_id_2'],
    )
    dish_count = len(
        await dish_repo.get_all_dishes(
            session=session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2']
        )
    )

    assert dish
    assert response.status_code == 201
    assert response.json()['id'] == str(dish.id)
    assert response.json()['title'] == data['title'] == dish.title
    assert response.json()['description'] == data['description'] == dish.description
    assert response.json()['price'] == data['price'] == str(dish.price)
    assert dish_count == 1

    ids_data['dish_id_3'] = response.json()['id']

    data = {'title': 'Test CRUD submenu title #4', 'description': 'Test CRUD submenu description #4', 'price': '10.00'}
    response = await ac.post(
        reverse('dish_create', menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3']), json=data
    )
    dish = await dish_repo.get_one_or_none_dish(
        session=session,
        dish_id=response.json()['id'],
        menu_id=ids_data['menu_id_2'],
        submenu_id=ids_data['submenu_id_3'],
    )
    dish_count = len(
        await dish_repo.get_all_dishes(
            session=session, menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3']
        )
    )

    assert dish
    assert response.status_code == 201
    assert response.json()['id'] == str(dish.id)
    assert response.json()['title'] == data['title'] == dish.title
    assert response.json()['description'] == data['description'] == dish.description
    assert response.json()['price'] == data['price'] == str(dish.price)
    assert dish_count == 1

    ids_data['dish_id_4'] = response.json()['id']


async def test_counts(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, submenu_repo: SubMenuRepository, dish_repo: DishRepository
):
    """Проверяю количество подменю и блюд в меню"""
    response = await ac.get(reverse('menu_retrieve', menu_id=ids_data['menu_id_1']))

    assert response.status_code == 200
    assert response.json()['id'] == ids_data['menu_id_1']

    submenus_count = len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_1']))
    dishes_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1'])
    ) + len(await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2']))

    assert response.json()['submenus_count'] == submenus_count == 2
    assert response.json()['dishes_count'] == dishes_count == 3

    response = await ac.get(reverse('menu_retrieve', menu_id=ids_data['menu_id_2']))

    assert response.status_code == 200
    assert response.json()['id'] == ids_data['menu_id_2']

    submenus_count = len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_2']))
    dishes_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3'])
    )

    assert response.json()['submenus_count'] == submenus_count == 1
    assert response.json()['dishes_count'] == dishes_count == 1


async def test_counts_submenu_delete(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, submenu_repo: SubMenuRepository, dish_repo: DishRepository
):
    """Удаляю первое подменю и проверяю количество подменю и блюд в первом меню"""
    response = await ac.delete(
        reverse('submenu_delete', menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1'])
    )
    dish_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1'])
    )

    assert response.status_code == 200
    assert len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_1'])) == 1
    assert dish_count == 0


async def test_counts_after_delete_submenu(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, submenu_repo: SubMenuRepository, dish_repo: DishRepository
):
    """Проверяю количество подменю и блюд в меню после удаления первого подменю"""
    response = await ac.get(reverse('menu_retrieve', menu_id=ids_data['menu_id_1']))

    assert response.status_code == 200
    assert response.json()['id'] == ids_data['menu_id_1']

    submenus_count = len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_1']))
    dishes_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1'])
    ) + len(await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2']))

    assert response.json()['submenus_count'] == submenus_count == 1
    assert response.json()['dishes_count'] == dishes_count == 1

    response = await ac.get(reverse('menu_retrieve', menu_id=ids_data['menu_id_2']))

    assert response.status_code == 200
    assert response.json()['id'] == ids_data['menu_id_2']

    submenus_count = len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_2']))
    dishes_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3'])
    )

    assert response.json()['submenus_count'] == submenus_count == 1
    assert response.json()['dishes_count'] == dishes_count == 1


async def test_counts_submenu_delete_all(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, submenu_repo: SubMenuRepository, dish_repo: DishRepository
):
    """Удаляю все подменю и проверяю количество подменю и блюд"""
    response = await ac.delete(
        reverse('submenu_delete', menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2'])
    )
    dish_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2'])
    )

    assert response.status_code == 200
    assert len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_1'])) == 0
    assert dish_count == 0

    response = await ac.delete(
        reverse('submenu_delete', menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3'])
    )
    dish_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3'])
    )

    assert response.status_code == 200
    assert len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_2'])) == 0
    assert dish_count == 0


async def test_counts_after_delete_all(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, submenu_repo: SubMenuRepository, dish_repo: DishRepository
):
    """Проверяю количество подменю и блюд в меню после удаления всех подменю"""
    response = await ac.get(reverse('menu_retrieve', menu_id=ids_data['menu_id_1']))

    assert response.status_code == 200
    assert response.json()['id'] == ids_data['menu_id_1']

    submenus_count = len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_1']))
    dishes_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_1'])
    ) + len(await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_1'], submenu_id=ids_data['submenu_id_2']))

    assert response.json()['submenus_count'] == submenus_count == 0
    assert response.json()['dishes_count'] == dishes_count == 0

    response = await ac.get(reverse('menu_retrieve', menu_id=ids_data['menu_id_2']))

    assert response.status_code == 200
    assert response.json()['id'] == ids_data['menu_id_2']

    submenus_count = len(await submenu_repo.get_all_with_counts(session, menu_id=ids_data['menu_id_2']))
    dishes_count = len(
        await dish_repo.get_all_dishes(session, menu_id=ids_data['menu_id_2'], submenu_id=ids_data['submenu_id_3'])
    )

    assert response.json()['submenus_count'] == submenus_count == 0
    assert response.json()['dishes_count'] == dishes_count == 0


async def test_counts_delete_all_menus(
    ac: AsyncClient, session: AsyncSession, ids_data: dict, menu_repo: MenuRepository
):
    """Удаляю все меню"""
    response = await ac.delete(reverse('menu_delete', menu_id=ids_data['menu_id_1']))

    assert response.status_code == 200
    assert len(await menu_repo.get_all(session)) == 1

    response = await ac.delete(reverse('menu_delete', menu_id=ids_data['menu_id_2']))

    assert response.status_code == 200
    assert len(await menu_repo.get_all(session)) == 0
