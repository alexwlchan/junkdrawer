FROM python:3-alpine

RUN pip install youtube-dl

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["youtube-dl"]
