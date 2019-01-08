FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "A wrapper for woff2 compression utils from https://github.com/google/woff2"

RUN apk add --no-cache --update build-base git
RUN git clone --recursive https://github.com/google/woff2.git

WORKDIR woff2
RUN make all
