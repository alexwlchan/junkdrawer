FROM alpine

RUN apk add --update sassc

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["sassc"]
