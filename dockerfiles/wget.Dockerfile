FROM alpine

RUN apk update && apk add ca-certificates wget

ENTRYPOINT ["/usr/bin/wget"]
