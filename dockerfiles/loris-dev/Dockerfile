FROM ubuntu:16.04

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "A Docker image for doing local Loris development"

RUN apt-get update

RUN apt-get install -y python python-pip python-setuptools python-dev \
    uwsgi-plugin-python libjpeg-turbo8-dev libfreetype6-dev zlib1g-dev \
    liblcms2-dev liblcms2-utils libtiff5-dev libwebp-dev libffi-dev libssl-dev

COPY requirements.txt .
COPY requirements_test.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements_test.txt

VOLUME /repo
WORKDIR /repo
