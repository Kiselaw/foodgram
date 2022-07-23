# Foodgram

The **Foodgram** project is a platform that allows users to share their recipes.

## Overview

The foodgram platform implements all the basic functionality inherent in projects of this kind.

Users can:
- register and create recipes
- subscribe to other users, thus forming their own recipe feed
- filter recipes by tags
- add recipes to favorites and shopping list (which can be downloaded as a txt file)

In addition, the Foodgram project has CI/CD which is implemented via using the Github Actions, so when push happens, the code is automatically tested and deployed to a remote server.

## Technologies
Backend:

- Python 3.9.5
- Django
- Djnago REST framework
- Docker

Frontend:

- JavaScript
- React

## Installation and launch

### Clone the repository and go to it using the command line:

```bash
git clone https://github.com/Kiselaw/foodgram-project-react

cd foodgram-project-react
```

### Create and activate a virtual environment

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

### Install dependencies from a file requirements.txt

```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

### Make migrations

Windows: 

```bash
py manage.py migrate
```

macOS/Linux:

```bash
python3 manage.py migrate
```

### Launch

Windows:

```bash
py manage.py runserver
```

macOS/Linux:

```bash
python3 manage.py runserver
```

### Commands for uploading data from csv files

Windows:

```bash
py manage.py csv_import --<command> <file path>

--ingredient - command to load ingredients 
```

macOS/Linux:

```bash
python3 manage.py csv_import --<command> <file path>

--ingredient - command to load ingredients 
```

### Commands for pre-filling database

```bash
py manage.py loadata <filename>

tags.json - сommand to load tags
users.json - command to load users
```

## Examples of API requests

### User registration algorithm

1. The user sends a POST request to add a new user with the following parameters: email, password, username, first_name, last_name to the /api/users/ endpoint.
2. The user sends a POST request to receive a token for authentication to the api/token/login/ endpoint.

### API root endpoint (links to resources available in the API):

[http://127.0.0.1:8000/api/](http://localhost/api/)

Detailed description is in [Documentation](http://localhost/api/docs/).

### Commands to launch the project in Docker containers:
```bash
1. `docker-compose up -d --build` - building/rebuilding containers
2. `winpty docker-compose exec django python manage.py makemigrations` - creating migrations
3. `winpty docker-compose exec django python manage.py migrate` - making migration
4. `winpty docker-compose exec django python manage.py createsuperuser` - creation of superuser
5. `winpty docker-compose exec django python manage.py collectstatic --no-input` - collecting static files
6. `docker-compose down -v` - stopping the container and removing dependecies
```

## Project status

At the moment, it is planned to remove SerializerMethodField from sterilizers and search for a more correct and "beautiful" solution.

http://84.201.177.249/ - link to the deployed project

## License

MIT


![Foodgram workflow](https://github.com/Kiselaw/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
