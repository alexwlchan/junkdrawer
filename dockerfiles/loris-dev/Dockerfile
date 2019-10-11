FROM ubuntu:16.04

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "A Docker image for doing local Loris development"

RUN apt-get update

RUN apt-get install -y python3 python3-setuptools python3-dev \
    uwsgi-plugin-python3 libjpeg-turbo8-dev libfreetype6-dev zlib1g-dev \
    liblcms2-dev liblcms2-utils libtiff5-dev libwebp-dev libffi-dev libssl-dev

COPY requirements.txt .
COPY requirements_test.txt .

RUN apt-get install -y python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements_test.txt

VOLUME /repo
WORKDIR /repo
