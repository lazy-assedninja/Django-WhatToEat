# Django-WhatToEat
Refactor the university project.

## Environment
* Ubuntu 16.04.7 LTS
* MySQL Client 14.14
* MySQL Server 5.7.3-log
* Python 3.7.10 (line-bot-sdk require version >= 3.6)

## Virtual environment
To avoid the following error when creating virtual environment on Ubuntu:
```commandline
The virtual environment was not created successfully because ensurepip is not available.  On Debian/Ubuntu systems, you need to install the python3-venv package using the following command.
   apt install python3-venv
You may need to use sudo with that command.  After installing the python3-venv package, recreate your virtual environment.
```
```commandline
Error: Command '['/home/eddie/Slask/tmp/venv/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1
```
Install the python3-venv package and use the virtualenv command instead, virtualenv called `venv`:
```commandline
sudo apt install python3-venv python-virtualenv
virtualenv --python=python3.7 venv
```
Start your virtual environment:
```commandline
source venv/bin/activate
```
Install MySQL developing packages:
```commandline
sudo apt-get install libmysqlclient-dev python-dev
```
Install packages with requirements:
```commandline
pip install -r requirements.txt
```

## Configurations
To use python-dotenv, create the `.env` file, it can include various server parameters.
```
SECRET_KEY = 'SECRET_KEY'
ALLOWED_HOSTS = '*'

DB_ENGINE = 'django.db.backends.mysql'
DB_NAME = 'DB_NAME'
DB_USER = 'DB_USER'
DB_PASSWORD = 'DB_PASSWORD'
DB_HOST = 'localhost'
DB_PORT = '3306'

LINE_CHANNEL_ACCESS_LONG_TOKEN = 'LINE_CHANNEL_ACCESS_LONG_TOKEN'
LINE_CHANNEL_SECRET = 'LINE_CHANNEL_SECRET'
```

## Run
You need to be in the directory that contains the manage.py file, execute the following command to start the server:
```commandline
python3 manage.py runserver
```