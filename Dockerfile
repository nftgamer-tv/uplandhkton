# Dockerfile
FROM python:3.9.4-slim


RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY app/ .