# Variables
DOCKER_COMPOSE = docker compose

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make deploy 	     - Deploy services (build, test, and run)"
	@echo "  make build          - Build Docker images"
	@echo "  make clean          - Remove all Docker images, containers, and volumes"
	@echo "  make test           - Run unit tests"

# Build Docker images
.PHONY: deploy
deploy: test build

# Deploy services
.PHONY: build
build:
	$(DOCKER_COMPOSE) up --build -d

# Destroy depolyment
.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# Run unit tests (Blocking - stops if tests fail)
.PHONY: test
test:
	@echo "Running tests..."
	@docker run --rm -v $(PWD)/gateway_service:/app -w /app python:3.13.2-slim \
		sh -c "pip install -r requirements.txt && PYTHONPATH=/app pytest tests/"
	@echo "✅ Tests passed! Proceeding to deployment..."
