<h1>Описание</h1>

Домашние задания интенсива Ylab.

<h1>Выполненные задания со звездочкой</h1>


<h3>Дз №2</h3>

Условие №3 (сложный ORM запрос) [**app/repositories/menu.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/repositories/menu.py)

Условие №4 (тест кол-ва подменю/блюд) [**app/tests/menu_tests/test_crud_menu_counts.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/tests/menu_tests/test_crud_menu_counts.py)


<h3>Дз №3</h3>

Условие №5 (описать эндпоинты) [**app/routes**](https://github.com/Bish0p-r/fastapi-ylab/tree/master/app/routes)

Условие №6 (функция reverse()) [**app/tests/utils.py**](https://github.com/Bish0p-r/fastapi-ylab/blob/master/app/tests/utils.py)


<h3>Дз №4</h3>

Условие №5 (обновление меню из google sheets) [**...**]()

Условие №6 (блюда по акции) [**...**]()


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
