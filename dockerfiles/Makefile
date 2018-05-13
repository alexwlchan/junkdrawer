ROOT = $(shell git rev-parse --show-toplevel)
DOCKERFILES = $(ROOT)/dockerfiles

IMAGES = atool lessc optipng primitive tiny_elastic travis wget youtube_dl


define __template
$(ROOT)/.docker/$(1): $(DOCKERFILES)/$(1).Dockerfile
	docker build --tag alexwlchan/$(1) --file $(DOCKERFILES)/$(1).Dockerfile $(DOCKERFILES)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/$(1)

docker-$(1)-build: $(ROOT)/.docker/$(1)
endef


$(foreach img,$(IMAGES),$(eval $(call __template,$(img))))
