<h1>Описание</h1>

Домашние задания интенсива Ylab.

<h1>Выполненные задания со звездочкой</h1>


<h3>Дз №2</h3>

Условие №3 (сложный ORM запрос): [**app/repositories/menu.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/repositories/menu.py)

Условие №4 (тест кол-ва подменю/блюд): [**app/tests/menu_tests/test_crud_menu_counts.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/tests/menu_tests/test_crud_menu_counts.py)


<h3>Дз №3</h3>

Условие №5 (описать эндпоинты): [**app/routes**](https://github.com/Bish0p-r/fastapi-ylab/tree/master/app/routes)

Условие №6 (функция reverse()): [**app/tests/utils.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/tests/utils.py)


<h3>Дз №4</h3>

Условие №5 (обновление меню из google sheets): [**app/tasks/excel_to_db.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/tasks/excel_to_db.py)
* Можете проверить работоспособность приложения с моей [ссылкой](https://docs.google.com/spreadsheets/d/1LRTFejM3Po-I5i6moHvloF_yhmKUsTW8/edit#gid=1700880523) (она открыта для редактирования) либо укажите в .env файле ваш айди ссылки в поле **GOOGLE_SHEETS_ID**, если айди будет указан неверно парсится будет файл в директории **admin/Menu.xlsx**, логи того что именно спарсилось можно посмотреть в контейнере **ylab_celery**.
* Основная логика синхронизации описана в сервисе: [**app/services/admin.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/services/admin.py)
* Логика парсинга находится в директории: [**app/common/utils/excel_parser.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/common/utils/excel_parser.py)

Условие №6 (блюда по акции): [**app/models/dish.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/models/dish.py#L18)
* Реализовал путем добавления поля "discount" для блюд, расчет цены с учетом скидки происходит в pydantic схеме: [**app/schemas/dish.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/schemas/dish.py#L27)

Тест нового эндпоинта: [**app/tests/menu_tests/test_crud_menu_tree.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/tests/menu_tests/test_crud_menu_tree.py)

Исправления ДЗ №4:
* Удалил поле "discount" из модели Dish, теперь скидки хранятся в кэше в формате Dish.id: discount
* Логика расчета цены с учетом скидки происходит в сервисном слое: [**app/services/dish.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/services/dish.py#L91)
* Скидки теперь парсятся отдельно [**app/common/utils/excel_parser.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/common/utils/excel_parser.py#L42)

<h1>Установка</h1>

1. **Клонируйте репозиторий.**
```bash
git clone https://github.com/Bish0p-r/fastapi-ylab
```
2. **Перейдите в директорию проекта.**
```bash
cd fastapi-ylab
```
3. **Переименуйте ".env.example" в ".env".**
4. **Запустите докер контейнер.**
```bash
docker-compose up -d --build
```
* Чтобы прошли postman тесты, необходимо запустить без фоновой задачи celery, для этого используйте эту команду.
```bash
docker-compose up -d --build db redis app
```
5. Приложение будет доступно по адресу: `http://localhost:8000/`

<h1>Тестирование</h1>

1. Выполните первые 3 пункта установки.
2. Запустите контейнер с тестами с помощью команды:
```bash
docker-compose -f docker-compose-test.yaml up --build
```
>После выполнения всех тестов контейнер завершит работу.
> Прогресс выполнения тестов отображается в логах контейнера "ylab_app_test"

* Если логи не отображаются попробуйте запустить с помощью этой команды:

```bash
docker-compose -f docker-compose-test.yaml up -d --build && docker logs --follow ylab_app_test
```
