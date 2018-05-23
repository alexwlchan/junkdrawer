FROM alpine

RUN apk add --update \
  --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
  atool unrar

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["atool"]
