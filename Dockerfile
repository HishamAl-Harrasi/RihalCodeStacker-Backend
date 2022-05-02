FROM python:3.9-slim

COPY ./src /app/src

COPY  requirements.txt /app
COPY  install.sh /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN /bin/bash install.sh

WORKDIR /app/src

EXPOSE 8000
