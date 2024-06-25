project_dir := .
bot_dir := bot

.PHONY: lint
lint:
	@poetry run ruff check $(project_dir)
	@poetry run mypy $(project_dir) --strict

.PHONY: format
format:
	@poetry run ruff check $(project_dir) --fix