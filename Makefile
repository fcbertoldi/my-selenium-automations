VENV_NAME = my-selenium-automations

lock: requirements.txt

lock-dev: requirements.txt requirements-dev.txt

requirements.txt: pyproject.toml
	pip-compile -o requirements.txt pyproject.toml

requirements-dev.txt: requirements.txt
	pip-compile --extra dev -o requirements-dev.txt requirements.txt pyproject.toml

sync:
	pip-sync requirements.txt

sync-dev:
	pew in $(VENV_NAME) pip-sync requirements.txt requirements-dev.txt

install:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt $(VENV_NAME)

.PHONY: sync sync-dev install
