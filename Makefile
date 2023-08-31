VENV_NAME = my-selenium-automations

lock: requirements.txt requirements-dev.txt

requirements.txt: requirements.in

requirements-dev.txt: requirements.txt requirements-dev.in

%.txt: %.in
	pew in $(VENV_NAME) pip-compile --output-file $@ $<

sync:
	pew in $(VENV_NAME) pip-sync requirements.txt requirements-dev.txt

install:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt $(VENV_NAME)

.PHONY: sync install
