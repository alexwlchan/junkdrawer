FROM golang:alpine

RUN apk add --update git
RUN go get github.com/aws/aws-sdk-go/

VOLUME ["/go/src"]
WORKDIR ["/go/src"]

ENTRYPOINT ["go", "build"]
