FROM python:3-alpine

RUN pip3 install twine

ENTRYPOINT ["twine"]
