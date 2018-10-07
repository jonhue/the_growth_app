FROM python:3
MAINTAINER Jonas Hübotter

WORKDIR /usr/src/app

ENV SECRET_KEY XXX

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
