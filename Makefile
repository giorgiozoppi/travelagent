# Detect if uv is available, otherwise use pip
UV := $(shell command -v uv 2> /dev/null)
ifdef UV
    PIP := uv pip
    PIP_INSTALL := uv pip install
else
    PIP := pip
    PIP_INSTALL := pip install
endif

.PHONY: help install install-dev install-uv clean lint format type-check test test-unit test-integration test-cov check build run

help:
	@echo "Available targets:"
	@echo "  install          - Install package dependencies (auto-detects uv/pip)"
	@echo "  install-dev      - Install package with dev dependencies (auto-detects uv/pip)"
	@echo "  install-uv       - Install uv package manager"
	@echo "  clean            - Remove build artifacts and cache files"
	@echo "  lint             - Run ruff linter"
	@echo "  format           - Format code with ruff"
	@echo "  type-check       - Run mypy type checking"
	@echo "  test             - Run all pytest tests"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-cov         - Run tests with coverage report"
	@echo "  check            - Run all checks (lint, format-check, type-check)"
	@echo "  build            - Build the package"
	@echo "  run              - Run the travel agent application"
	@echo ""
	@echo "Current package manager: $(PIP)"

install:
	@echo "Installing with $(PIP)..."
	$(PIP_INSTALL) -e .

install-dev:
	@echo "Installing dev dependencies with $(PIP)..."
	$(PIP_INSTALL) -e ".[dev]"

install-uv:
	@echo "Installing uv package manager..."
	@command -v uv >/dev/null 2>&1 || { \
		echo "uv not found. Installing via pip..."; \
		pip install uv; \
	}
	@echo "uv is installed!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	ruff check .

format:
	ruff format .
	ruff check --select I --fix .

format-check:
	ruff format --check .

type-check:
	mypy travelagent/

test:
	pytest -v

test-unit:
	pytest tests/unit -v

test-integration:
	pytest tests/integration -v

test-cov:
	pytest --cov=travelagent --cov-report=html --cov-report=term-missing -v

check: lint format-check type-check
	@echo "All checks passed!"

build:
	python -m build

run:
	python -m travelagent.main
