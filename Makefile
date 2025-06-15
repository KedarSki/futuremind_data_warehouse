#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := $(shell pwd)

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

.PHONY: poetry-install-deps
poetry-install-deps:
	poetry install --with dev

#* Dev environment
.PHONY: activate
activate:
	poetry shell

#* Linting & Testing
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=src tests/

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml ./

.PHONY: black_check
black_check:
	poetry run black --diff --check .

.PHONY: pylint
pylint:
	poetry run pylint -j 4 src/

.PHONY: check-all
check-all: black_check pylint mypy test

.PHONY: run-distributors
run-distributors:
	poetry run python -m src.pipeline.distributor_loader

.PHONY: run-oracle_connection
run-oracle_connection:
	poetry run python -m src.oracle_connection

.PHONY: run-movies
run-movies:
	poetry run python -m src.pipeline.movie_loader

.PHONY: run-facts
run-facts:
	poetry run python -m src.pipeline.fact_revenue_loader