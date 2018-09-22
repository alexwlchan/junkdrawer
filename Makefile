ROOT = $(shell git rev-parse --show-toplevel)

include alfred_workflow/Makefile
include safari-stylesheet/Makefile
include textmate-config/Makefile

safari-stylesheet/style.css: $(ROOT)/safari-stylesheet/style.css

~/.config/fish/config.fish:
	mkdir -p ~/.config/fish
	echo ". $(ROOT)/fishconfig/config.fish" >> ~/.config/fish/config.fish
