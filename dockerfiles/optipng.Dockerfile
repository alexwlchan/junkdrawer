FROM alpine

RUN apk update && apk add optipng

ENTRYPOINT ["/usr/bin/optipng"]
