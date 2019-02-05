IMAGE = alexwlchan/rack-test-bug

.docker: Dockerfile
	docker build -t $(IMAGE) .
	touch .docker

run: .docker
	docker run --volume $(CURDIR):/data --publish 8282:8282 $(IMAGE) server.rb

test: .docker
	docker run --volume $(CURDIR):/data $(IMAGE) test.rb
