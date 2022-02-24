SHELL := /bin/bash

install:
	python3.10 -m venv venv; \
	source venv/bin/activate; \
	pip3 install --upgrade pip; \
	pip3 install -r requirements.txt; \
	deactivate;

clean:
	@echo "Deleting virtual environment and python cache ..."; \
	rm -rf venv; \
	find . -type d -name __pycache__ -exec rm -r {} \+;
