ROOT = $(shell git rev-parse --show-toplevel)
PINCE = $(ROOT)/pdf-manager

$(PINCE)/requirements.txt: $(PINCE)/requirements.in
	docker run --rm --tty --volume $(PINCE):/src micktwomey/pip-tools
