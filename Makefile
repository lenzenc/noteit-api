.PHONY: help install setup dev test test-cov lint format type-check quality clean
.PHONY: infra-up infra-down infra-logs infra-clean
.PHONY: docker-build docker-run docker-stop

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
install: ## Install dependencies with Poetry
	poetry install

setup: install ## Complete project setup (install deps + create .env)
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "✅ Created .env file. Edit it with your specific configuration."; \
	else \
		echo "✅ .env file already exists."; \
	fi

# Development
dev: ## Run development server with auto-reload
	poetry run python scripts/dev.py

dev-debug: ## Run development server with debug logging
	PYTHONPATH=src poetry run uvicorn noteit_api.main:app --host 0.0.0.0 --port 8000 --reload --reload-dirs src/ --log-level debug

# Testing
test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage report
	poetry run pytest --cov=src/noteit_api --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	poetry run pytest --looponfail

# Code Quality
lint: ## Run linting (flake8)
	poetry run flake8 src/ tests/

format: ## Format code with black and isort
	poetry run black src/ tests/
	poetry run isort src/ tests/

format-check: ## Check code formatting without making changes
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/

type-check: ## Run type checking with mypy
	poetry run mypy src/

quality: format lint type-check ## Run all code quality checks

quality-check: format-check lint type-check ## Check code quality without making changes

# Infrastructure Management
infra-up: ## Start infrastructure services (MinIO, ImgProxy)
	docker-compose up -d

infra-down: ## Stop infrastructure services
	docker-compose down

infra-logs: ## View infrastructure logs
	docker-compose logs -f

infra-clean: ## Stop services and remove volumes
	docker-compose down -v

infra-restart: infra-down infra-up ## Restart infrastructure services

# Full Application Management
up: infra-up dev ## Start infrastructure and run development server

down: infra-down ## Stop all services

restart: down up ## Restart everything

# Cleanup
clean: ## Clean up temporary files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

clean-all: clean infra-clean ## Clean everything including Docker volumes

# Docker (for production builds)
docker-build: ## Build Docker image
	docker build -t noteit-api .

docker-run: ## Run application in Docker container
	docker run -p 8000:8000 --env-file .env noteit-api

docker-stop: ## Stop Docker container
	docker stop $$(docker ps -q --filter ancestor=noteit-api)

# Development helpers
shell: ## Open Poetry shell
	poetry shell

deps-update: ## Update dependencies
	poetry update

deps-show: ## Show dependency tree
	poetry show --tree

# Quick start for new developers
quickstart: setup infra-up ## Complete setup for new developers
	@echo "🚀 Quick start complete!"
	@echo "💡 Run 'make dev' to start the development server"
	@echo "📖 API docs will be available at: http://localhost:8000/docs"