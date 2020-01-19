ROOT = $(shell git rev-parse --show-toplevel)
DIR = $(ROOT)/2017


$(DIR)/.docker/gobuilder: $(DIR)/builder.Dockerfile
	docker build --tag alexwlchan/gobuilder --file builder.Dockerfile $(DIR)
	mkdir -p $(DIR)/.docker
	touch $(DIR)/.docker/gobuilder

$(DIR)/.docker/gorunner: $(DIR)/runner.Dockerfile
	docker build --tag alexwlchan/gorunner --file runner.Dockerfile $(DIR)
	mkdir -p $(DIR)/.docker
	touch $(DIR)/.docker/gorunner

%.out: $(DIR)/.docker/gobuilder %.go
	docker run --rm --volume $(DIR):/src --workdir /src alexwlchan/gobuilder \
		-o /src/$@ /src/$(shell basename $@ .out).go
