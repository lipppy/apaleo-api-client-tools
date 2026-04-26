# Makefile for generating Python models from OpenAPI specifications
PWD := $(shell pwd)

format:
	@echo "Formatting code with isort and black..."
	poetry run isort .
	poetry run black .
	@echo "Code formatting completed."
