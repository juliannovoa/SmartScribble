# SmartScribble

The aim of this project is to develop a tool for assisted text writing by using the latest advances in Natural Language Processing. For this purpose, a web application has been developed in which users can register, create text documents, edit them and delete them. While editing the documents, the user gets a suggestion of the word that should appear next in the text. 

## Install dependencies

```shell
# apt install mariadb-server libmariadb-dev
# apt install python3-pip python3-dev
# apt install python3-venv
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
$ cd SmartScribble/
$ python3.7 -m venv .
$ source bin/activate
$ pip3 install -r SmartScribble/requirements.txt
```

```shell
$ cd src/
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
```

## Test the app

```shell
$ python3 manage.py runserver
```

## Alternative: Docker

Donwload Dockerfile from repository

```shell
$ docker build -t app .
$ docker run -p 8000:8000 app
```
