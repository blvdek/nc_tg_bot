""" """
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

MIN_CHUNK_SIZE = 5242880
MAX_CHUNK_SIZE = 5368709120


class Database(BaseModel):
    """Represent database connection settings."""

    host: str
    user: str
    name: str
    password: str
    port: int = 5432
    driver: str = "asyncpg"
    database_system: str = "postgresql"

    @property
    def url(self) -> str:
        """Construct and return the SQLAlchemy URL based on the database settings.

        :return: The SQLAlchemy URL for the database connection.
        """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


class Redis(BaseModel):
    """Represent Redis connection settings."""

    host: str
    db: int = 1
    port: int = 6379
    user: str | None = None
    password: str | None = None
    state_ttl: int | None = None
    data_ttl: int | None = None


class Webhook(BaseModel):
    """Represent settings for a webhook endpoint."""

    host: str
    port: int
    url: str
    path: str
    secret: str | None = None


class Nextcloud(BaseModel):
    """Represent Nextcloud connection settings."""

    protocol: str = "https"
    host: str
    port: int = 80
    chunk_size: int = 5242880

    @property
    def url(self) -> str:
        """ """
        return f"{self.protocol}://{self.host}:{self.port}"

    @field_validator("chunk_size")
    @classmethod
    def check_chunk_size(cls, v: int) -> int:
        """ """
        if MIN_CHUNK_SIZE > v > MAX_CHUNK_SIZE:
            msg = "The size of chunks must be between 5MB and 5GB."
            raise ValueError(msg)
        return v


class Telegram(BaseModel):
    """Represents Telegram bot settings"""

    token: str
    chunk_size: int = 5242880
    max_upload_size: int = 20971520


class Settings(BaseSettings):
    """Represents the configuration settings for the bot"""

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
