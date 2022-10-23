.SILENT:

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_RED = \033[31m
PROJECT_NAME = `basename $(PWD)`

.DEFAULT_GOAL = help

PATH_PYTHON=./app_python
PATH_PHP=./app_php

## Prints this help.
help:
	printf "${COLOR_YELLOW}\n${PROJECT_NAME}\n\n${${COLOR_YELLOW}}"
	awk '/^[a-zA-Z\-\_0-9\.%]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "${COLOR_GREEN}$$ make %s${COLOR_YELLOW} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	printf "\n"

## Start local setup
local-setup:
	pip install -r requirements.txt
	
## Make Python Class
python-compiler:
	python -m grpc_tools.protoc \
	--proto_path=${PWD} \
	--python_out=${PATH_PYTHON} \
	--grpc_python_out=${PATH_PYTHON} \
	${PWD}/proto/calculations.proto

## Make Python Class
python-server:
	python ${PATH_PYTHON}/server.py

## Make Python Class
python-client:
	python ${PATH_PYTHON}/client.py