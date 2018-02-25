FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "A Docker image that wraps the travis-ci command-line tool"

RUN apk update
RUN apk add git ruby ruby-dev
RUN apk add build-base libffi-dev ruby-irb ruby-rdoc && \
    gem install travis && \
    apk del build-base libffi-dev

VOLUME /repo
WORKDIR /repo

ENTRYPOINT ["/usr/bin/travis"]
