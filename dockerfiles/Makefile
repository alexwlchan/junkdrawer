ROOT = $(shell git rev-parse --show-toplevel)
DOCKERFILES = $(ROOT)/dockerfiles

<<<<<<< Updated upstream
IMAGES = \
<<<<<<< HEAD
	atool \
	dos2unix \
	ffmpeg \
	gotutorial \
	lessc \
	primitive \
	sass \
	tiny_elastic \
	travis \
	tree \
	woff2
=======
	primitive \
	tiny_elastic
>>>>>>> 960d1f7ced4ea529789700c67450ed34fe944543
=======
IMAGES = primitive
>>>>>>> Stashed changes


define __template
$(ROOT)/.docker/$(1): $(DOCKERFILES)/$(1).Dockerfile
	docker build --tag alexwlchan/$(1) --file $(DOCKERFILES)/$(1).Dockerfile $(DOCKERFILES)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/$(1)

docker-$(1)-build: $(ROOT)/.docker/$(1)
endef


$(foreach img,$(IMAGES),$(eval $(call __template,$(img))))
