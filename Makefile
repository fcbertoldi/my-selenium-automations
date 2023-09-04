VENV_NAME = my-selenium-automations

lock: requirements.txt requirements-dev.txt

requirements.txt: requirements.in

requirements-dev.txt: requirements.txt requirements-dev.in

%.txt: %.in
	pew in $(VENV_NAME) pip-compile --output-file $@ $<

sync:
	pew in $(VENV_NAME) pip-sync requirements.txt requirements-dev.txt

build-pkg:
	pew in $(VENV_NAME) python -m build

install-dev:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt $(VENV_NAME)
	pew in $(VENV_NAME) python -m pip install -e .

install:
	pipx install -e .

clean:
	rm -rf dist/

.PHONY: sync build-pkg install-dev install clean
