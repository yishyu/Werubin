# Werubin
Web Technologies Travel App Project

# Start Project
First start by cloning this repo :)
## Install Requirements
we are using poetry to manage our packages
```bash
pip install poetry
poetry install
```
## Init Environment variables
Create an environment file
```bash
touch .env
```
Put the following variable in .env

(email_host and pass is referring to the email address who will be sending the email)

Note: the current servers are set to ovh's, also email sending is disable when debug is True

.env
```
SECRET_KEY=devkey
ALLOWED_HOSTS=127.0.0.1
DEBUG=1
EMAIL_HOST=test@test.com
EMAIL_PASSWORD=emailpassword
```

## Launch app
```bash
poetry shell
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
Go to http://127.0.0.1:8000/ and log in with credential you used in createsuperuser.

Note: the username is used to log in and not the email !