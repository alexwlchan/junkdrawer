ROOT = $(shell git rev-parse --show-toplevel)
AWS = $(ROOT)/aws


$(ROOT)/.docker/gobuilder: $(AWS)/Dockerfile
	docker build --tag alexwlchan/gobuilder $(AWS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/gobuilder

gobuilder = $(ROOT)/.docker/gobuilder


%.out: gobuilder %.go
	docker run --rm --volume $(AWS):/go/src alexwlchan/gobuilder \
		-o /go/src/$@ /go/src/$(shell basename $@ .out).go

run-%: %.out
	@docker run --rm --volume $(AWS):/bin tianon/true /bin/"$(subst run-,,$@).out"
