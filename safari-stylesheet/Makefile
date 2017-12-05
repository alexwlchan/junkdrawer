ROOT = $(shell git rev-parse --show-toplevel)
SAFARI = $(ROOT)/safari-stylesheet

$(ROOT)/.docker/safari_stylesheet: $(SAFARI)/Dockerfile
	docker build --tag safari_stylesheet $(SAFARI)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/safari_stylesheet

$(SAFARI)/style.css: $(ROOT)/.docker/safari_stylesheet $(SAFARI)/%.less
	docker run --volume $(SAFARI):/data safari_stylesheet
