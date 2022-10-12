FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN mkdir /logs

# upgrade pip
RUN pip install --upgrade pip

# install gdal
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# install mysql-server
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential


# install dependancy
RUN pip install -r requirements.txt

# COPY ./entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
