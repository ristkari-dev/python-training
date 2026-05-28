SHELL := /bin/bash
.DEFAULT_GOAL := help

REPO_ROOT := $(shell pwd)

.PHONY: help
help: ## List available targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: sync
sync: ## Install/refresh the workspace venv (uv sync --all-packages)
	uv sync --all-packages

.PHONY: test
test: ## Run solution tests (the ones that should always pass)
	@dirs=$$(find lessons -type d -name solutions 2>/dev/null); \
	if [ -z "$$dirs" ]; then echo "no solution directories yet"; else uv run pytest tools $$dirs; fi

.PHONY: test-exercises
test-exercises: ## Run exercise tests (these fail by design until students complete them)
	-@dirs=$$(find lessons -type d -name exercises 2>/dev/null); \
	if [ -z "$$dirs" ]; then echo "no exercise directories yet"; exit 0; fi; \
	uv run pytest $$dirs

.PHONY: test-lesson
test-lesson: ## Run tests for one lesson, both exercises and solutions (LESSON=NN-name)
	@test -n "$(LESSON)" || (echo "usage: make test-lesson LESSON=NN-name" && exit 1)
	-uv run pytest lessons/$(LESSON)/exercises
	uv run pytest lessons/$(LESSON)/solutions

.PHONY: lint
lint: ## Run ruff check
	uv run ruff check .

.PHONY: fmt
fmt: ## Format with ruff format + ruff check --fix
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: typecheck
typecheck: ## Run mypy on tools and lesson solutions
	uv run mypy tools/new_lesson/src tools/slides_dev/src

.PHONY: new-lesson
new-lesson: ## Scaffold a new lesson (NAME=NN-name)
	@test -n "$(NAME)" || (echo "usage: make new-lesson NAME=NN-name" && exit 1)
	uv run python -m new_lesson $(NAME)

.PHONY: slides-dev
slides-dev: ## Serve one lesson's deck locally on http://localhost:8000 (LESSON=NN-name)
	@test -n "$(LESSON)" || (echo "usage: make slides-dev LESSON=NN-name" && exit 1)
	uv run python -m slides_dev --lesson $(LESSON) --repo-root $(REPO_ROOT)
