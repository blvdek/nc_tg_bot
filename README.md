<p align="center">
    <img src="https://raw.githubusercontent.com/blvdek/nc_tg_bot/main/assets/logo.png" width="250" alt="NcPyApi logo">
</p>

<h1 align="center"><em>Nextcloud Telegram Bot</em></h1>

<p align="center">
  <a href="https://hub.docker.com/r/bagoont/nc_tg_bot"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/bagoont/nc_tg_bot?logo=docker"></a>
  <a href="https://www.python.org/downloads"><img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python"></a>
  <a href="https://github.com/blvdek/nc_tg_bot/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Code style"></a>
<p>

## 🤖 About Nextcloud Telegram Bot

This Telegram bot simplifies the process of interacting with Nextcloud, allowing users to easily share files without navigating the Nextcloud interface directly. It also provides the following functionalities:

- File management: users can navigate through the file hierarchy and manage files and folders.
- Trash bin management: users can restore or delete files from the trash bin.
- Search by name: users can search for files by their name.

Much more can be easily implemented using the nc_py_api and aigoram libraries.


## ❓Motivation

I created a Telegram bot to simplify sharing memes on Nextcloud for myself and friends. It provides a user-friendly interface for efficient communication and collaboration. The project streamlines the sharing process and enhances efficiency. This experience will be valuable in my future projects involving external service integration with Telegram.


## 🚀 How to Use

> 💡Installation presupposes that Nextcloud is already installed and configured.

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

- Install dependencies using [Poetry](https://python-poetry.org "python package manager"):
```bash
poetry install
```

- Start the necessary services (at least the database and redis)

- Create and edit .env file:
```bash
cp .env.exmaple .env
vi .env
```

-   Make migrations:
```bash
make migrate
```

- Start telegram bot:
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
| `NC__OVERWRITE__PROTOCOL`  | External accessible protocol.                                                               |
| `NC__OVERWRITE__HOST`      | External accessible hostname.                                                               |
| `NC__OVERWRITE__PORT`      | External accessible hostname.                                                               |
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


## ☁️ Docker and Nextcloud

To use the Nextcloud Telegram bot with Nextcloud, you can create a Docker Compose file that runs on the same Docker network as Nextcloud. This allows the bot to communicate with Nextcloud internally.

To do this, you need to set the NC__PROTOCOL, NC__HOST and NC__PORT environment variables in your Docker Compose file or .env. These variables are used for internal communication between bot and Nextcloud.

If the internal and external host are different, you can set the NC__OVERWRITE__PROTOCOL, NC__OVERWRITE__HOST and NC__OVERWRITE__PORT variables. These variables are used for the external access link that the bot will send.

If your NC__PROTOCOL, NC__HOST and NC__PORT are already accessible from outside, you don't need to specify NC__OVERWRITE__PROTOCOL, NC__OVERWRITE__HOST and NC__OVERWRITE__PORT. In this case, the bot will use NC__PROTOCOL, NC__HOST and NC__PORT as the external access points.

> 💡For example, you set the parameters of the docker internal network for NC__HOST and other default variables, then links of the following type will be created: http://nextcloud:80/... The user will not be able to open such links in browser, but if you specify OVERWRITE, the host will be replaced with OVERWRITE and the links will look like, for example: https://exmaple.com:80/... and the user will already be able to open such links in his browser.

Here's an example of how you can configure this in your Docker Compose file:

```docker
services:

...

# For example, here is an NGINX container that receives an ssl certificate
# and indicates that the domain "example.com" points to the Nextcloud container.

...

  nextcloud:
    image: nextcloud
    ports:
      - 8080:80
    volumes:
      - nextcloud-data:/var/www/html
    networks:
      - nextcloud-network

...

volumes:
  nextcloud-data:

networks:
  nextcloud-network:
    name: nextcloud-network
    driver: bridge
```

Docker compose file with bot:

```docker
services:

...

  bot:
    image: bagoont/nc_tg_bot
    restart: always
    env_file: .env
    environment:
      NC__HOST: "nextcloud"
      NC__OVERWRITE__PROTOCOL: "https"
      NC__OVERWRITE__HOST: "example.com"
      NC__OVERWRITE__PORT: 80
    volumes:
      - data:/var/www/html
    network:
      - nextcloud-host-network

...

volumes:
  data:

networks:
  nextcloud-host-network:
    name: nextcloud-network
    external: true
```

## ⚙️ Tech Stack
- [poetry](https://python-poetry.org/) — development workflow.
- [docker](https://www.docker.com/) — to automate deployment.
- [postgres](https://www.postgresql.org/) — powerful, open source object-relational database system.
- [asyncpg](https://github.com/MagicStack/asyncpg) — a fast PostgreSQL Database Client Library for Python/asyncio.
- [alembic](https://github.com/sqlalchemy/alembic) — a database migrations tool for SQLAlchemy.
- [redis](https://redis.io/) — in-memory data structure store used as a cache and FSM.
- [aiogram](https://aiogram.dev/) — asynchronous framework for Telegram Bot API.
- [aiogram_i18n](https://github.com/aiogram/i18n) — middleware for Telegram bot internationalization.
- [fluent-runtime](https://projectfluent.org/) — a localization system.
- [pydantic-settings](https://github.com/pydantic/pydantic-settings) — settings management using pydantic.
- [sqlalchemy](https://www.sqlalchemy.org/) — object-relational mapping (ORM) library that provides a set of high-level API for interacting with relational databases
- [uvloop](https://github.com/MagicStack/uvloop) — ultra fast asyncio event loop.
- [nc-py-api](https://github.com/cloud-py-api/nc_py_api) — Nextcloud Python framework.
- [mypy](https://www.mypy-lang.org/) — optional static typing for Python.
- [ruff](https://docs.astral.sh/ruff/) — an extremely fast Python linter and code formatter, written in Rust.
- [pre-commit](https://pre-commit.com/) — a framework for managing and maintaining multi-language pre-commit hooks.


## ⭐ Support
If you find this project useful, you can support it in the following ways:

- [🌟 Star](https://github.com/blvdek/nc_tg_bot/stargazers) the repository.
- [💬 Contribute](https://github.com/blvdek/nc_tg_bot/blob/main/.github/CONTRIBUTING.md) to the project.
- [📣 Share](https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fblvdek%2Fnc_tg_bot&text=Nextcloud%20Telegram%20Bot) this project on social media.


## ❗ More information

- [Contribute](https://github.com/blvdek/nc_tg_bot/blob/main/.github/CONTRIBUTING.md)
  - [Discussions](https://github.com/blvdek/nc_tg_bot/discussions)
  - [Issues](https://github.com/blvdek/nc_tg_bot/issues)
