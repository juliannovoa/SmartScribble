# SmartScribble

## Install dependencies

```shell
# apt install mariadb-server libmariadb-dev
# apt install python3-pip python3-dev
```

## Create database

```mysql
CREATE DATABASE smartscribbledb;
CREATE USER 'django'@'%' IDENTIFIED BY 'SmartMariaScribbleDB2000!';
GRANT ALL ON smartscribbledb.* TO 'django'@'%';
GRANT ALL ON test_smartscribbledb.* TO 'django'@'%';
```

## Download web app

```shell
$ git clone https://github.com/juliannovoa/SmartScribble.git
$ pip3 install -r SmartScribble/requirements.txt
```

```shell
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
```

## Test the app

```shell
$ python3 manage.py runserver
```
