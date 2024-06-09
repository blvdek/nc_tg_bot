"""This file contains middleware for providing "LocalizedTranslator" object"""

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

if TYPE_CHECKING:
    from bot.language import Translator


class TranslatorMD(BaseMiddleware):
    """Middleware for providing "LocalizedTranslator" object."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Add "LocalizedTranslator" object to the conextual data.

        :param handler: Wrapped handler in middlewares chain
        :param event: Incoming event
        :param data: Contextual data. Will be mapped to handler arguments
        :return: Handler with updated contextual data
        """
        hub: Translator | None = data.get("_translator_hub")
        if hub is None:
            msg = "'Translator' object not found."
            raise RuntimeError(msg)
        data["translator"] = hub(language=event.from_user.language_code)
        return await handler(event, data)
