# loris-dev

This is the Docker image I use for doing local development work on the [Loris image server][loris].
My daily work environment is macOS, and Kakadu and OpenJPEG are particularly slow there – so I find it faster to run them in a Linux container.

For example, to run all the Loris tests:

```console
$ cd /path/to/loris-repo
$ docker build -f /path/to/dockerfiles/loris-dev/Dockerfile -t loris-dev .
$ docker run -v $(pwd):/repo loris-dev coverage run --module py.test --verbose tests/*.py && coverage report
```

[loris]: https://github.com/loris-imageserver/loris
