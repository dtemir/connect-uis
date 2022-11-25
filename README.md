# connect-uis
Connect at the University of Illinois Springfield!

# Contribute

Take the following steps to setup the environment and start contributing to **connect-uis**.

## Setup Environment

Create a Python virtual environment to keep your global libaries clean.

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ python3 -m pip install -r requirements.txt
```

## Setup Database

Setup a SQLite database for Django and create an admin user.

```bash
# create a secret Django key in your local directory
(venv) $ echo "export SECRET_KEY='$(openssl rand -hex 40)'" > .env
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

If you change anything in a file titled `models.py` that defines the database schema, make sure to make migrations and apply them.

```bash
(venv) $ python3 manage.py makemigrations
(venv) $ python3 manage.py migrate
```

## Run Locally

With the help of a WSGI application server Gunicorn, you can run the site locally.

```bash
(venv) $ gunicorn -c config/gunicorn/dev.py
```

If you end up bringing the website to production with Nginx, domain name and SSL certificate ([Certbot](https://certbot.eff.org/)), make sure to use the Gunicorn production script.

```bash
(venv) $ gunicorn -c config/gunicorn/prod.py
```


## Setup Twillio and SendGrid Integration

Please reference the following documentation on [Send Email Verifications with Verify and Twilio SendGrid](https://www.twilio.com/docs/verify/email?code-sample=code-start-a-verification-with-email&code-language=Python&code-sdk-version=7.x)

You will need to create an `.env` file in `blog/` directory and specify the following
```bash
export ACCOUNT_SID='ACXXXXXXXXXXXXXXXXXXXX'
export AUTH_TOKEN='bdXXXXXXXXXXXXXXXXXXXX'
export VERIFY_SERVICES='VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

![Email Showing Verification Code to Register](docs/email-verification.png)

## Visualize System

If you would like to do show the interaction between models you created, run this command.

```bash
(venv) $ ./manage.py graph_models -a -I Profile,Post,UpvotePost,Follow,User -o blog-graph.png
```

![UIS Connect's System Visualized in a Graph](docs/blog-graph.png)