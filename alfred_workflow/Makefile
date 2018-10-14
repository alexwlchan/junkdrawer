ROOT = $(shell git rev-parse --show-toplevel)

ALFRED = $(ROOT)/alfred_workflow
BUILD_IMAGE = alexwlchan/build_alfred_workflow

$(ALFRED)/requirements.txt: $(ALFRED)/requirements.in
	docker run --volume $(ALFRED):/src --rm --tty micktwomey/pip-tools

$(ROOT)/.docker/alfred: $(ALFRED)/requirements.txt
	docker build --tag $(BUILD_IMAGE) $(ALFRED)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/alfred

deps = \
	$(ALFRED)/alfred_shortcuts.yml \
	$(ALFRED)/build_alfred_workflow.py \
	$(wildcard $(ALFRED)/icons/*.png) \
	$(wildcard $(ALFRED)/scripts/*)

$(ALFRED)/junkdrawer.alfredworkflow: $(ROOT)/.docker/alfred $(deps)
	docker run --tty --rm --volume $(ALFRED):/data $(BUILD_IMAGE)
	open $(ALFRED)/junkdrawer.alfredworkflow

junkdrawer.alfredworkflow: $(ALFRED)/junkdrawer.alfredworkflow
