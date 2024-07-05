"""i18n locale manager."""
from aiogram.types import User as TgUser
from aiogram_i18n.managers import BaseManager


class LocaleManager(BaseManager):
    """Managing locales. Just returns the locale specified in the telegram."""

    async def get_locale(self, event_from_user: TgUser | None = None) -> str:
        """Returns locale of the user."""
        if event_from_user is None:
            raise ValueError
        if event_from_user.language_code is None:
            raise ValueError
        return event_from_user.language_code

    async def set_locale(self) -> None:
        """Does nothing."""
