FROM alpine

RUN apk add --update cloc

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["cloc"]
