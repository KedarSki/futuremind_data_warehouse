.PHONY: install run test lint fmt check-all clean activate

# Poetry-based Makefile — all commands go through poetry

install:
	poetry install

run:
	poetry run python src/main.py

test:
	poetry run pytest tests/

lint:
	poetry run flake8 src/

fmt:
	poetry run black src/ tests/

check-all: fmt lint

clean:
	del /Q /F *.pyc
	del /Q /F */__pycache__/*

activate:
	@echo "To enter poetry virtualenv, run:"
	@echo "poetry shell"
