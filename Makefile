VENV_NAME = my-selenium-automations
UV_TOOL := $(shell command -v uv)

ifeq ($(UV_TOOL),)
	PIP := python -m pip
	PIP_COMPILE := pip-compile
	PIP_SYNC := pip-sync --pip-args "--no-deps"
else
	PIP := $(UV_TOOL) pip
	PIP_COMPILE := $(UV_TOOL) pip compile
	PIP_SYNC := $(UV_TOOL) pip sync
endif


lock: requirements.txt requirements-dev.txt

requirements.txt: requirements.in

requirements-dev.txt: requirements.txt requirements-dev.in

%.txt: %.in
	pew in $(VENV_NAME) $(PIP_COMPILE) --output-file $@ $<

sync:
	pew in $(VENV_NAME) $(PIP_SYNC) requirements.txt requirements-dev.txt

build-pkg:
	pew in $(VENV_NAME) python -m build

install-dev:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt $(VENV_NAME)
	pew in $(VENV_NAME) $(PIP) install -e .

install:
	pipx install -e .

clean:
	fd -t d __pycache__ . -x rm -rf
	rm -rf dist/

.PHONY: sync build-pkg install-dev install clean
