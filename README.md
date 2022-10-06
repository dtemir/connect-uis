# connect-uis
Connect at the University of Illinois Springfield!

# Contribute

Take the following steps to setup the environment and start contributing to **connect-uis**.

## Setup Environment

Create a Python virtual environment to keep your global libaries clean.

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ python3 -m pip install requirements.txt
```

## Setup Database

Setup a SQLite database for Django and create an admin user.

```bash
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py createsuperuser
Username: admin
Email address: admin@gmail.com
Password: 
Password (again):
Superuser created successfully.
(venv) $ python3 manage.py runserver # 0:8000 if running on a remote server
```

Head over to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and see that everything is running correctly.

## Model changes

If you change anything in a file titled `models.py` that defines the database schema, make sure to make migrations and apply them

```bash
(venv) $ python3 manage.py makemigrations
(venv) $ python3 manage.py migrate
```