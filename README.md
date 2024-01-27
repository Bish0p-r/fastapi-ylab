<h1>Описание</h1>

Домашние задания интенсива Ylab.

Реализацию условия №3 второго дз можно найти по пути **app/repositories/menu.py**

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
docker-compose up -d
```
5. Приложение будет доступно по адресу: `http://localhost:8000/`

<h1>Тестирование</h1>

1. Выполните первые 3 пункта установки.
2. Запустите контейнер с тестами с помощью команды:
```bash
docker-compose -f docker-compose-test.yaml up
```
>После выполнения всех тестов контейнер завершит работу.
> Прогресс выполнения тестов отображается в логах контейнера "ylab_app_test"

* Если логи не отображаются попробуйте запустить с помощью этой команды:

```bash
docker-compose -f docker-compose-test.yaml up -d && docker logs --follow ylab_app_test
```

