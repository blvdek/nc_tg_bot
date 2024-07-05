"""Configuration settings for the Nextcloud Telegram Bot.

This module contains classes that define the configuration settings necessary for the operation
of the Nextcloud Telegram Bot. These settings include database connection details, Redis
configuration, webhook settings, Nextcloud server details, and Telegram bot credentials.
"""
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

MIN_CHUNK_SIZE = 5242880
MAX_CHUNK_SIZE = 5368709120


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
    name: str
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
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


class Redis(BaseModel):
    """Configuration for connecting to a Redis cache.

    Redis connection settings are optional and fall back to in-memory storage if not provided.

    :param host: The hostname of the Redis server.
    :param db: The database number within Redis to connect to, defaults to 1.
    :param port: The port number on which the Redis server listens, defaults to 6379.
    :param user: The username for Redis authentication, defaults to None.
    :param password: The password for Redis authentication, defaults to None.
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

    Webhook settings are optional and are used when the bot is configured to receive updates via a webhook.

    :param host: The hostname where the webhook should be hosted.
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


class Nextcloud(BaseModel):
    """Configuration to communicate with a Nextcloud server.

    :param protocol: The protocol used to communicate with the Nextcloud server, defaults to "https".
    :param host: The hostname of the Nextcloud server.
    :param port: The port number on which the Nextcloud server listens, defaults to 80.
    :param chunk_size: The maximum size of file chunks for uploads, defaults to 5242880.
    """

    protocol: str = "https"
    host: str
    port: int = 80
    chunk_size: int = 5242880

    @property
    def url(self) -> str:
        """Constructs and returns the URL for connecting to the Nextcloud server."""
        return f"{self.protocol}://{self.host}:{self.port}"

    @field_validator("chunk_size")
    @classmethod
    def check_chunk_size(cls, v: int) -> int:
        """Validates the chunk size against minimum and maximum limits."""
        if MIN_CHUNK_SIZE > v > MAX_CHUNK_SIZE:
            msg = f"The size of chunks must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}."
            raise ValueError(msg)
        return v


class Telegram(BaseModel):
    """Configuration specific to the Telegram bot, such as the bot token and upload limits.

    :param token: The token used to authenticate the bot with the Telegram API.
    :param page_size: The number of items to fetch per request, defaults to 8.
    :param max_upload_size: The maximum size of a file that can be uploaded, defaults to 20971520.
    :param drop_pending_updates: Whether to drop pending updates on bot restart, defaults to True.
    """

    token: str
    page_size: int = 8
    max_upload_size: int = 20971520
    drop_pending_updates: bool = True


class Settings(BaseSettings):
    """Configuration in a single object.

    :param model_config: Configuration options for Pydantic settings, including environment file paths.
    :param appname: The name of the application, defaults to "Nextcloud Telegram Bot".
    :param logging: The logging level, defaults to "INFO".
    :param telegram: An instance of :class:`Telegram` containing Telegram-specific settings.
    :param nextcloud: An instance of :class:`Nextcloud` containing Nextcloud-specific settings.
    :param db: An instance of :class:`Database` containing database connection settings.
    :param redis: An instance of :class:`Redis` containing Redis connection settings, defaults to None.
    :param webhook: An instance of :class:`Webhook` containing webhook settings, defaults to None.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
    )
    appname: str = "Nextcloud Telegram Bot"
    logging: str = "INFO"
    telegram: Telegram
    nextcloud: Nextcloud
    db: Database
    redis: Redis | None = None
    webhook: Webhook | None = None


settings = Settings()
