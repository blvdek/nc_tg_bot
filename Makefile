project_dir := .
bot_dir := bot
translations_dir := bot/locales

.PHONY: lint
lint:
	ruff check $(bot_dir)
	mypy $(bot_dir) --strict

.PHONY: format
format:
	ruff check $(bot_dir) --fix

.PHONY: migrate
migrate:
	alembic upgrade head
