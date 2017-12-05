ROOT = $(shell git rev-parse --show-toplevel)
SAFARI = $(ROOT)/safari-stylesheet

include $(ROOT)/dockerfiles/Makefile

$(SAFARI)/style.css: $(ROOT)/.docker/lessc $(wildcard $(SAFARI)/*.scss)
	docker run --volume $(SAFARI):/data alexwlchan/lessc style.scss style.css
