FROM node:alpine

RUN npm install -g less

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["lessc"]
