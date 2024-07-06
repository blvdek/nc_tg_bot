project_dir := .
bot_dir := bot
translations_dir := bot/locales

.PHONY: lint
lint:
	ruff check $(project_dir)
	mypy $(project_dir) --strict

.PHONY: format
format:
	ruff check $(project_dir) --fix

.PHONY: migrate
migrate:
	alembic upgrade head
