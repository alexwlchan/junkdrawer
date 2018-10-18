FROM alpine

RUN apk add --update ffmpeg

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["ffmpeg"]
