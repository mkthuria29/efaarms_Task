FROM python:3.8-slim-buster

ENV TZ=Asia/Kolkata

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY src /app/
