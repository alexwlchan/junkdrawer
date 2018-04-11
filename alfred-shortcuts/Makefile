ROOT = $(shell git rev-parse --show-toplevel)

ALFRED = $(ROOT)/alfred-shortcuts
BUILD_IMAGE = alexwlchan/build_alfred_workflow

$(ALFRED)/requirements.txt: $(ALFRED)/requirements.in
	docker run --volume $(ALFRED):/src --rm --tty micktwomey/pip-tools

$(ROOT)/.docker/alfred: $(ALFRED)/requirements.txt $(ALFRED)/build_alfred_workflow.py
	docker build --tag $(BUILD_IMAGE) $(ALFRED)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/alfred

$(ALFRED)/web-links.alfredworkflow: $(ROOT)/.docker/alfred $(wildcard $(ALFRED)/icons/*.png)
	docker run --tty --rm --volume $(ALFRED):/data $(BUILD_IMAGE)

web-links.alfredworkflow: $(ALFRED)/web-links.alfredworkflow
