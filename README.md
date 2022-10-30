## <h1 align="center"> Продуктовый помощник </h1>

### Описание проекта

Сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. Работа приложения осуществляется через виртуальный сервер на Yandex.Cloud и контейнеризацию.

## Шаблон наполнения .env файла для работы с базой данных

Создайте файл .env с переменными окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql <в проекте используется postgresql>
DB_NAME=<имя базы данных>
POSTGRES_USER=<логин для подключения к базе данных>
POSTGRES_PASSWORD=<пароль для подключения к БД>
DB_HOST=<название сервиса (контейнера)>
DB_PORT=<порт для подключения к БД>
```
### Сборка и запуск приложения

Перейти в папку infra/

```
docker-compose build
docker-compose up -d
```

### Выполнение миграций

```
docker-compose exec web python manage.py migrate
```

### Создание суперпользователя

```
docker-compose exec web python manage.py createsuperuser
```

### Сборка статики

```
docker-compose exec web python manage.py collectstatic --no-input
```
### Экспорт данных в файл

```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

### Загрузка данных из файла

```
docker-compose exec web python manage.py loaddata fixtures.json
```

### Остановка приложения

```
docker-compose down
```

## http://178.154.222.160/

