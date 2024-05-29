# Cinema Reservation

a simple cinema reservation app that depends on django and django-rest-framework using default token auth for drf

## Features

- [Halls](#hall-section)
- [Movies](#movie-section)
- [Reservations](#movie-section)
- [Users](#User-section)

## Installaion

<h6 style="color:green">Ensure you have pipenv installed locally then catch up</h6>

cd into desired directory

```
git clone https://github.com/Yossef-Elshafey/tickets-api
```

cd into tickets-api

```
pipenv install --dev
```

- this would create a virtual environment using pipenv
- install packages includes devel

activate your venv

```
pipenv shell
```

#### Migrations

migrations for django/drf(sessions,tables,auth-token,etc.. ) \
migrations for the apps

```
python manage.py makemigrations
python manage.py makemigrations hall movies reservation users
```

```
python manage.py migrate
```

at this point you should run server without any errors

```
python manage.py runserver
```

# To be continue
