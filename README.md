<h1>Описание</h1>

API для работы с меню, подменю и блюдами.

<h1>Tech stack</h1>

* **Python 3.10**
* **FastAPI**
* **PostgreSQL + async SQLAlchemy + asyncpg driver**
* **Redis**
* **Celery**
* **Rabbitmq**
* **Pytest**
* **Docker + docker-compose**


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
