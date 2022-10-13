FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .
RUN mkdir /logs

# update apt-get
RUN apt-get update

# upgrade pip
RUN pip install --upgrade pip

# install mysql-server
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

# install dependancy
RUN pip install -r requirements.txt
