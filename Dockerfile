FROM python:3.7-alpine
MAINTAINER Daniel gabay.

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /dabert
WORKDIR /dabert
COPY ./dabert /dabert

# Create & Select user with run privileges only (-D).
RUN adduser -D user
USER user
