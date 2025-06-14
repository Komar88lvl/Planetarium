# Planetarium API

Welcome to the "CENTAURI" planetarium

This project is a management system for a planetarium.
It allows administrators to create sessions, assign topics to each session,
link them to specific halls, and manage ticket reservations.

---


## 🛠 Technologies

- Python 3.12
- Django 5.2.1
- Django REST Framework 3.16.0
- PostgresQL
- Docker & Docker Compose
- Simple JWT 5.5.0 for authentication

---


## Features
- Creating & manage astronomy themes, shows
- Creating planetarium domes (halls)
- A flexible ticket reservation system
- Registration with email
- Filtering astronomy show by themes
- Filtering shao session show by show date, planetarium dome & astronomy show
- Admin panel /admin/
- JWT authenticated
- Documentation is located at api/v1/doc/swagger/ or api/v1/doc/redoc/


## Installing using GitHub
This project use postgres db, so you need create it first

- git clone https://github.com/Komar88lvl/Planetarium.git
- cd planetarium
- python3 -m venv venv | python -m venv venv (for windows)
- source venv/bin/activate | venv\Scripts\activate (for windows)
- pip install -r requirements.txt
- touch .env (fill in the .env file according to the .env.sample)
- python manage.py migrate
- python manage.py runserver

After this steps service will be available at http://127.0.0.1:8000/  

you might create superuser
- python manage.py createsuperuser

Or create common user at http://127.0.0.1:8000/api/v1/user/register/

## Run with docker

docker should be installed
- docker-compose up --build  
service will be available at http://127.0.0.1:8001/


## Features of use

After getting access you can test swagger or redoc api documentation with your access token
- http://127.0.0.1:8000/api/v1/doc/swagger/
- http://127.0.0.1:8000/pi/v1/doc/redoc/

Also you can check if your token still available (it works for 1 hour) at:
- http://127.0.0.1:8000/api/v1/user/token/verify/

Refresh token, if it`s need (using a refresh token) at:
- http://127.0.0.1:8000/api/v1/user/token/refresh/

Check and update your account information at:

- http://127.0.0.1:8000/api/v1/user/me/
