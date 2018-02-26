FROM python:3-alpine

RUN apk update && apk add ffmpeg

RUN pip install youtube-dl

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["youtube-dl"]
