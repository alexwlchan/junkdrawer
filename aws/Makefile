ROOT = $(shell git rev-parse --show-toplevel)
AWS = $(ROOT)/aws


$(ROOT)/.docker/gobuilder: $(AWS)/builder.Dockerfile
	docker build --tag alexwlchan/gobuilder --file builder.Dockerfile $(AWS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/gobuilder

$(ROOT)/.docker/gorunner: $(AWS)/runner.Dockerfile
	docker build --tag alexwlchan/gorunner --file runner.Dockerfile $(AWS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/gorunner

%.out: $(ROOT)/.docker/gobuilder %.go
	docker run --rm --volume $(AWS):/src --workdir /src alexwlchan/gobuilder \
		-o /src/$@ /src/$(shell basename $@ .out).go
