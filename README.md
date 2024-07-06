<p align="center">
    <img src="https://raw.githubusercontent.com/blvdek/nc_tg_bot/tests/assets/logo.png" width="250" alt="NcPyApi logo">
</p>

<h1 align="center"><em>Nextcloud Telegram Bot</em></h1>

<p align="center">
  <a href="https://github.com/donBarbos/telegram-bot-template/actions/workflows/linters.yml"><img src="https://img.shields.io/github/actions/workflow/status/blvdek/nc_tg_bot/linters.yml?label=linters" alt="Linters Status"></a>
  <a href="https://github.com/donBarbos/telegram-bot-template/actions/workflows/docker-image.yml"><img src="https://img.shields.io/github/actions/workflow/status/blvdek/nc_tg_bot/docker-image.yml?label=docker%20image" alt="Docker Build Status"></a>
  <a href="https://www.python.org/downloads"><img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python"></a>
  <a href="https://github.com/blvdek/nc_tg_bot/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Code style"></a>
<p>

## ❓Motivation

## 🚀 How to Use

### 🐳 Running in Docker _(recommended method)_

- Create and edit .env file:
```bash
cp .env.exmaple .env
vi .env
```

- Start services:
```bash
docker compose up -d
```

### 💻 Running on Local Machine

- Install dependencies using [Poetry](https://python-poetry.org "python package manager")
```bash
poetry install
```

- Start the necessary services (at least the database and redis)

- Create and edit .env file:
```bash
cp .env.exmaple .env
vi .env
```

-   make migrations
```bash
make migrate
```

- Start telegram bot.
```bash
poetry run python -m bot
```

## 🌍 Environment variables

To launch the bot you only need a token bot, database, Redis and Nextcloud settings, everything else can be left out. For more information, see `.env.example`.

| Name                       | Description                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| `APPNAME`                  | Name of the application.                                                                    |
| `LOGGING`                  | Logging level.                                                                              |
| `TG__TOKEN`                | Token used to authenticate the bot with the Telegram API.                                   |
| `TG__PAGE_SIZE`            | Page size for pagination for Telegram API.                                                  |
| `TG__MAX_UPLOAD_SIZE`      | Maximum size of a file that can be uploaded.                                                |
| `TG__DROP_PENDING_UPDATES` | Whether to drop pending updates on bot restart.                                             |
| `TG__API_SERVER`           | The URL of the self-hosted Telegram API server.                                             |
| `NC__PROTOCOL`             | Protocol used to communicate with the Nextcloud server.                                     |
| `NC__HOST`                 | Hostname of the Nextcloud server.                                                           |
| `NC__PORT`                 | Port number on which the Nextcloud server listens.                                          |
| `NC__PUBLIC_PROTOCOL`      | Public protocol.                                                                            |
| `NC__PUBLIC_HOST`          | Public hostname.                                                                            |
| `NC__CHUNK_SIZE`           | Maximum size of file chunks for uploads.                                                    |
| `WEBHOOK__HOST`            | The hostname of webhook server.                                                             |
| `WEBHOOK__PORT`            | The port number on which the webhook server listens.                                        |
| `WEBHOOK__URL`             | The base URL for the webhook endpoint.                                                      |
| `WEBHOOK__PATH`            | The path under which the webhook endpoint is accessible.                                    |
| `WEBHOOK__SECRET`          | A secret token used for webhook verification.                                               |
| `REDIS__HOST`              | Hostname of the Redis server.                                                               |
| `REDIS__DB`                | Database number within Redis to connect to.                                                 |
| `REDIS__PORT`              | Port number on which the Redis server listens.                                              |
| `REDIS__USER`              | Uername for Redis authentication.                                                           |
| `REDIS__PASSWORD`          | Password for Redis authentication.                                                          |
| `REDIS__STATE_TTL`         | Time-to-live for state data in Redis.                                                       |
| `REDIS__DATA_TTL`          | Time-to-live for operational data in Redis.                                                 |
| `DB__HOST`                 | The hostname of the database server.                                                        |
| `DB__USER`                 | The username for database authentication.                                                   |
| `DB__DB`                   | The name of the database.                                                                   |
| `DB__PASSWORD`             | The password for database authentication.                                                   |
| `DB__PORT`                 | The port number on which the database server listens.                                       |
| `DB__DRIVER`               | The database driver to use.                                                                 |
| `DB__DATABASE_SYSTEM`      | The type of database system.                                                                |
