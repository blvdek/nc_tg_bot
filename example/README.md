# Example docker-compose with nextcloud, postgres, redis, webhook and self-hosted telegram api.

This Docker-compose file showcases how a bot interacts with other services. Please note that this example is not intended for production use.

> 💡Environment variables framed in `<>` characters are placeholders for your values.

Let's take a look at each service:
- **nextcloud:** A very simple nextcloud instance, needed just for an example. In the Nextcloud config, after instalation, you need to specify the names `nextcloud` and `<nextcloud-domain>` for 'trusted_domains'.

- **api-backend** and **api**: [Self-hosted telegram api](https://github.com/aiogram/telegram-bot-api) required in our case to increase download limits to 2 GB, but files will be saved locally in the volume `telegram-bot-api-data`. You will need to obtain `<api-id>` and `<api-hash>` as described in https://core.telegram.org/api/obtaining_api_id. Example is taken from this [repository](https://github.com/Olegt0rr/telegram-local).

- **redis**: Redis is used by bot for storing state data, which can be used to maintain user session data and track state changes.

- **db**: This postgres database is used for storing users.

- **bot**: Nextcloud telegram bot. You can see the description of the environment variables in the [README.md](https://github.com/blvdek/nc_tg_bot/blob/main/README.md) of this repository or in the [.env.example](https://github.com/blvdek/nc_tg_bot/blob/main/.env.example).

You need the `<nextcloud-domain>` point to port 8080 of the Nextcloud service and the domain from `<webhook-url>` point to the bot's webhook on port 8000.

After all preparations run:
```bash
docker compose up
```
