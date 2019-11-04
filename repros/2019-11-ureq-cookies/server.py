#!/usr/bin/env python
# -*- encoding: utf-8

import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    print("\nGot a request!")
    print("Headers: %r" % dict(flask.request.headers))
    print("Cookies: %r" % flask.request.cookies)
    return "hello world"


if __name__ == "__main__":
    app.run(port=5000)
