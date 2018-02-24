ROOT = $(shell git rev-parse --show-toplevel)

TM_CONFIG = $(ROOT)/textmate-config

APP_SUPPORT = ~/Library/Application\ Support/TextMate


$(APP_SUPPORT)/Global.tmProperties: $(TM_CONFIG)/Global.tmProperties
	rm -f $(APP_SUPPORT)/Global.tmProperties
	ln -s $(TM_CONFIG)/Global.tmProperties $(APP_SUPPORT)/Global.tmProperties


textmate-shortcuts: $(APP_SUPPORT)/Global.tmProperties
