project_dir := .
bot_dir := bot

# Lint code
.PHONY: lint
lint:
	@poetry run ruff check $(project_dir)
	@poetry run mypy $(project_dir) --strict

# format code
.PHONY: format
format:
	@poetry run ruff check $(project_dir) --fix