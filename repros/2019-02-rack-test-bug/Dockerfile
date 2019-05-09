FROM alpine

RUN echo "install: --no-rdoc --no-ri" > /root/.gemrc

RUN apk add --update build-base ruby ruby-dev
RUN gem install json minitest rack rack-test

EXPOSE 8282

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["ruby"]
