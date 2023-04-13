lock: requirements.txt

lock-dev: requirements.txt requirements-dev.txt

sync:
	pip-sync requirements.txt

sync-dev:
	pip-sync requirements.txt requirements-dev.txt

requirements-dev.txt: requirements.txt

%.txt: %.in
	pip-compile --output-file $@ $<

.PHONY: sync sync-dev
