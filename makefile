SHELL := /bin/bash
VENV := .env/bin

install:
	( \
		python3 -m venv .env; \
		source .env/bin/activate; \
		pip install -r requirements.txt; \
	)