ROOT = $(shell git rev-parse --show-toplevel)

include safari-stylesheet/Makefile

safari-stylesheet/style.css: $(ROOT)/safari-stylesheet/style.css
