ROOT = $(shell git rev-parse --show-toplevel)
AWS = $(ROOT)/aws


$(ROOT)/.docker/gobuilder: $(AWS)/Dockerfile
	docker build --tag alexwlchan/gobuilder $(AWS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/gobuilder

gobuilder: $(ROOT)/.docker/gobuilder


snssubscriptions: gobuilder snssubscriptions.go
	docker run --volume $(AWS):/go/src alexwlchan/gobuilder -o /go/src/snssubscriptions.out /go/src/snssubscriptions.go
