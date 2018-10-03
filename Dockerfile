FROM python:3.7
MAINTAINER Jonas Hübotter

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

ENV DATABASE_NAME postgres
ENV DATABASE_USER postgres
ENV DATABASE_HOST db
ENV DATABASE_PORT 5432
