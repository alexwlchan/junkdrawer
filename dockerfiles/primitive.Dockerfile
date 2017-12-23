FROM golang:1.8-alpine

RUN apk update && apk add git
RUN go get -u github.com/fogleman/primitive

WORKDIR /data
VOLUME /data

ENTRYPOINT ["primitive"]