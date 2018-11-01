FROM alpine

RUN apk add --update ca-certificates

ENV AWS_REGION=eu-west-1

VOLUME ["/bin"]
WORKDIR ["/bin"]
