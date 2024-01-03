FROM python:3.6.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app


COPY requirements.txt .


RUN python -m pip install -r requirements.txt


COPY . /app

ENV FLASK_APP=app_module



CMD flask run -h 0.0.0.0 -p $PORT

RUN flask db migrate -m "Initial migration"
RUN flask db upgrade
