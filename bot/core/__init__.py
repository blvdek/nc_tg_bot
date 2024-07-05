"""Core functionalities of the Nextcloud Telegram Bot."""
from .config import settings
from .loaders import _storage, bot, dp
from .runners import on_shutdown, on_startup, webhook_run, webhook_shutdown, webhook_startup

__all__ = (
    "settings",
    "bot",
    "dp",
    "_storage",
    "on_startup",
    "on_shutdown",
    "webhook_startup",
    "webhook_shutdown",
    "webhook_run",
)
