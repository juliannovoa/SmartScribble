# base image  
FROM python:3.7.3   

# setup environment variable  
ENV DockerHOME=/home/app  

# set work directory  
RUN mkdir -p $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV USE_SQLITE 1
  
# install dependencies  
RUN pip install --upgrade pip
  
# copy whole project to your docker home directory  
WORKDIR $DockerHOME
RUN git clone https://github.com/juliannovoa/SmartScribble.git  

# run this command to install all dependencies
WORKDIR $DockerHOME/SmartScribble
RUN pip install -r requirements.txt

WORKDIR $DockerHOME/SmartScribble/src

RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
