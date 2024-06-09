"""This file contains a localized text filter"""


from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from bot.language import LocalizedTranslator


class LocalizedTextFilter(BaseFilter):
    """Filter for checking if the text of the message matches the localized text for a given key"""

    def __init__(self, key: str) -> None:
        """Constructor method"""
        self.key = key

    async def __call__(self, event: TelegramObject, translator: LocalizedTranslator) -> bool:
        return event.text == translator.get(self.key)
