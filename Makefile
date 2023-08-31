RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RESET := \033[0m

.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@ poetry run pre-commit install
	@poetry shell

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 $(YELLOW)Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check$(RESET)"
	@poetry lock --check
	@echo "🚀 $(GREEN)Linting code: Running pre-commit$(RESET)"
	@poetry run pre-commit run -a
	@echo "🚀 $(RED)Static type checking: Running mypy$(RESET)"
	@poetry run mypy
	@echo "🚀 $(RED)Static type checking: Running pytype$(RESET)"
	@poetry run pytype
	@echo "🚀 $(YELLOW)Checking for obsolete dependencies: Running deptry$(RESET)"
	@poetry run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest --doctest-modules

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
