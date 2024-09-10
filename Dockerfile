# Start docker kernel + python
FROM python:3.12-slim-bullseye

# to show logs: python
ENV PYTHONUNBUFFERED = 1

# update kernel + install packages
RUN apt-get update && apt-get -y install gcc libpq-dev

# folder for my project
WORKDIR /app

# Copy Requirements
COPY requirements.txt /app/requirements.txt

# install req
RUN pip install -r /app/requirements.txt

# Copy all project files
COPY . /app/