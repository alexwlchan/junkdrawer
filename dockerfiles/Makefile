ROOT = $(shell git rev-parse --show-toplevel)
DOCKERFILES = $(ROOT)/dockerfiles

$(ROOT)/.docker/lessc: $(DOCKERFILES)/lessc.Dockerfile
	docker build --tag alexwlchan/lessc --file $(DOCKERFILES)/lessc.Dockerfile $(DOCKERFILES)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/lessc
