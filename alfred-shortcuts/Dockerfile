FROM alpine

RUN apk update && apk add python3 py3-pillow

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY build_alfred_workflow.py /build_alfred_workflow.py

WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["/build_alfred_workflow.py"]
