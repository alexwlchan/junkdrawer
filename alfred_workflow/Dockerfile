FROM alpine

RUN apk update && apk add python3 py3-pillow

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["/data/build_alfred_workflow.py"]
