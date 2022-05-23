# Описание проекта FOODGRAM-PROJECT-REACT

Проект **FOODGRAM-PROJECT-REACT** представляет собой платформу позволяющую пользователям делиться своими рецептами.


## Установка. Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Kiselaw/foodgram-project-react

cd foodgram-project-react
```

### Cоздать и активировать виртуальное окружение:

Windows:

```bash
py -3 -m venv env
```

```bash
. venv/Scripts/activate 
```

macOS/Linux:

```bash
python3 -m venv env

source env/bin/activate
```

### Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

### Выполнить миграции:

Windows: 

```bash
py manage.py migrate
```

macOS/Linux:

```bash
python3 manage.py migrate
```

### Запустить проект:

Windows:

```bash
py manage.py runserver
```

macOS/Linux:

```bash
python3 manage.py runserver
```

### Команды для загрузки данных из csv файлов

Windows:

```bash
py manage.py csv_import --<команда> <адрес_файла>

--ingredient - команда для загрузки ингредиентов из файла
```

macOS/Linux:

```bash
python3 manage.py csv_import --<команда> <адрес_файла>

--ingredient - команда для загрузки ингредиентов из файла
```

## Примеры запросов к API

### Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email, password, username, first_name, last_name на эндпоинт /api/users/.
2. Пользователь отправляет POST-запрос получение токен для аутентификации на эндпоинт api/token/login/. 

### Корневой эндпоинт API(ссылки на ресурсы, доступные в API):

[http://127.0.0.1:8000/api/](http://localhost/api/)

Подробное описание в [Документации](http://localhost/api/docs/).

### Команды для запуска проекта в контейнерах:
```bash
1. `docker-compose up -d --build` - сборка/пересборка контейнеров
2. `winpty docker-compose exec web python manage.py makemigrations` - создание новых миграций
3. `winpty docker-compose exec web python manage.py migrate` - применение миграций
4. `winpty docker-compose exec web python manage.py createsuperuser` - создание суперпользователя
5. `winpty docker-compose exec web python manage.py collectstatic --no-input` - собрать статические файлы
6. `docker-compose down -v` - остановка контейнеров и удаление зависимостей
```
http://84.201.177.249/ - ссылка на развернутый в котейнерах проект на сервере

![example workflow](https://github.com/Kiselaw/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)