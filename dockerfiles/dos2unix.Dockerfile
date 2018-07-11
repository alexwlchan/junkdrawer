FROM alpine

RUN apk add --update dos2unix

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["dos2unix"]
