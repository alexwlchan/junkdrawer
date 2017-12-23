ROOT = $(shell git rev-parse --show-toplevel)
DOCKERFILES = $(ROOT)/dockerfiles

define build_image
	docker build --tag alexwlchan/$(1) --file $(DOCKERFILES)/$(1).Dockerfile $(DOCKERFILES)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/$(1)
endef

$(ROOT)/.docker/lessc: $(DOCKERFILES)/lessc.Dockerfile
	$(call build_image,lessc)

$(ROOT)/.docker/primitive: $(DOCKERFILES)/primitive.Dockerfile
	$(call build_image,primitive)

$(ROOT)/.docker/youtube_dl: $(DOCKERFILES)/youtube_dl.Dockerfile
	$(call build_image,youtube_dl)
