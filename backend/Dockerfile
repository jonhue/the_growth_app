FROM python:3.7
MAINTAINER Jonas Hübotter

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN python manage.py migrate
ADD . /code/
