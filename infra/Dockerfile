FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt /app/

RUN apt-get update
RUN apt-get install -y gcc pkg-config

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app/
