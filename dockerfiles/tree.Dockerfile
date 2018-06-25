FROM alpine

RUN apk add --update --no-cache tree

WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["tree"]
