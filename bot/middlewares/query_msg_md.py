"""Query message middleware."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class QueryMsgMD(BaseMiddleware):
    """Retrieves the message associated with a callback query and check this message.

    If the message is inaccessible, it will answer with a message from i18n context.

    :param handler: The handler function to be executed.
    :param event: The event object.
    :param data: The data dictionary containing the request context.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Calls the handler function."""
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)
        if not isinstance(event.message, Message):
            i18n = data.get("i18n")
            if i18n is None:
                msg = "i18n context is required but was not provided."
                raise TypeError(msg)
            text = i18n.get("msg-is-inaccessible")
            await event.answer(text)
            return None
        return await handler(event, data)
