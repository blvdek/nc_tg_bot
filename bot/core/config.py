"""Configuration settings for the Nextcloud Telegram Bot.

This module contains classes that define the configuration settings necessary for the operation
of the Nextcloud Telegram Bot. These settings include database connection details, Redis
configuration, webhook settings, Nextcloud server details, and Telegram bot credentials.
"""

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

MAX_TG_FILE_SIZE = 2**31
MIN_CHUNK_SIZE = 5 * 2**20
MAX_CHUNK_SIZE = MAX_TG_FILE_SIZE


class Database(BaseModel):
    """Configuration for connecting to a database.

    :param host: The hostname of the database server.
    :param user: The username for database authentication.
    :param name: The name of the database.
    :param password: The password for database authentication.
    :param port: The port number on which the database server listens, defaults to 5432.
    :param driver: The database driver to use, defaults to "asyncpg".
    :param database_system: The type of database system, defaults to "postgresql".
    """

    host: str
    user: str
    db: str
    password: str
    port: int = 5432
    driver: str = "asyncpg"
    database_system: str = "postgresql"

    @property
    def url(self) -> str:
        """Construct and return the SQLAlchemy URL based on the database settings."""
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.db,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


class Redis(BaseModel):
    """Configuration for connecting to a Redis cache.

    Redis connection settings are optional and fall back to in-memory storage if not provided.

    :param host: Hostname of the Redis server.
    :param db: Database number within Redis to connect to, defaults to 1.
    :param port: Port number on which the Redis server listens, defaults to 6379.
    :param user: Uername for Redis authentication, defaults to None.
    :param password: Password for Redis authentication, defaults to None.
    :param state_ttl: Time-to-live for state data in Redis, defaults to None.
    :param data_ttl: Time-to-live for operational data in Redis, defaults to None.
    """

    host: str
    db: int = 1
    port: int = 6379
    user: str | None = None
    password: str | None = None
    state_ttl: int | None = None
    data_ttl: int | None = None


class Webhook(BaseModel):
    """Configuration for a webhook endpoint.

    Webhook settings are optional and are used when the bot is configured
    to receive updates via a webhook.

    :param host: The host of webhook.
    :param port: The port number on which the webhook server listens.
    :param url: The base URL for the webhook endpoint.
    :param path: The path under which the webhook endpoint is accessible.
    :param secret: A secret token used for webhook verification, defaults to None.
    """

    host: str
    port: int
    url: str
    path: str
    secret: str | None = None


class Overwrite(BaseModel):
    """Overwrite settings for Nextcloud server.

    It is used to overwrite the default url, for example, if the default url is not accessible
    from outside, and the user needs access to the link for authorization,
    than default url will be overwritten by this.

    :param protocol: Protocol used to communicate with the Nextcloud server.
    :param host: Hostname of the Nextcloud server.
    :param port: Port number on which the Nextcloud server listens.
    """

    protocol: str
    host: str
    port: int = 80


class Nextcloud(BaseModel):
    """Configuration to communicate with a Nextcloud server.

    :param protocol: Protocol used to communicate with the Nextcloud server, defaults to "https".
    :param host: Hostname of the Nextcloud server.
    :param port: Port number on which the Nextcloud server listens, defaults to 80.
    :param chunksize: Maximum size of file chunks for uploads, defaults to MIN_CHUNK_SIZE.
    :param overwrite: Overwrite settings for Nextcloud server, defaults to None.
    """

    protocol: str = "https"
    host: str
    port: int = 80
    chunksize: int = MIN_CHUNK_SIZE
    overwrite: Overwrite | None = None

    @property
    def url(self) -> str:
        """Constructs and returns the URL for connecting to the Nextcloud server."""
        return f"{self.protocol}://{self.host}:{self.port}"

    @field_validator("chunksize")
    @classmethod
    def check_chunksize(cls, v: int) -> int:
        """Validates the chunk size against minimum and maximum limits."""
        if MIN_CHUNK_SIZE > v > MAX_CHUNK_SIZE:
            msg = f"The size of chunks must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}."
            raise ValueError(msg)
        return v


class Telegram(BaseModel):
    """Configuration specific to the Telegram bot, such as the bot token and upload limits.

    :param token: Token used to authenticate the bot with the Telegram API.
    :param page_size: Page size for pagination for Telegram API, defaults to 8.
    :param max_upload_size: Maximum size of a file that can be uploaded, defaults to 20971520.
    :param drop_pending_updates: Whether to drop pending updates on bot restart, defaults to True.
    :param api_server: The URL of the Telegram API server, defaults to None.
    """

    token: str
    page_size: int = 8
    max_upload_size: int = 20971520
    drop_pending_updates: bool = True
    api_server: str | None = None

    @field_validator("max_upload_size")
    @classmethod
    def check_max_upload_size(cls, v: int) -> int:
        """Validates the max upload size against maximum limit."""
        if v > MAX_TG_FILE_SIZE:
            msg = f"The max size must be less than {MAX_TG_FILE_SIZE}."
            raise ValueError(msg)
        return v


class Settings(BaseSettings):
    """Configuration in a single object.

    :param model_config: Configuration options for Pydantic settings.
    :param appname: Name of the application, defaults to "Nextcloud Telegram Bot".
    :param logging: Logging level, defaults to "INFO".
    :param telegram: An instance of :class:`Telegram` containing Telegram-specific settings.
    :param nextcloud: An instance of :class:`Nextcloud` containing Nextcloud-specific settings.
    :param db: Containing database connection settings.
    :param redis: Containing Redis connection settings, defaults to None.
    :param webhook: Containing webhook settings, defaults to None.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    appname: str = "Nextcloud Telegram Bot"
    logging: str = "INFO"
    tg: Telegram
    nc: Nextcloud
    db: Database
    redis: Redis | None = None
    webhook: Webhook | None = None


settings = Settings()
