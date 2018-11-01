FROM golang:alpine

RUN apk add --update git
RUN go get github.com/aws/aws-sdk-go

VOLUME ["/src"]
WORKDIR ["/src"]

ENTRYPOINT ["go", "build"]
