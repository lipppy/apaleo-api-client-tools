# Makefile for generating Python models from OpenAPI specifications
PWD := $(shell pwd)

format:
	@echo "Formatting code with isort and ruff..."
	poetry run isort .
	poetry run ruff format .
	poetry run flake8 .
	poetry run mypy --strict .
	@echo "Code formatting completed."
