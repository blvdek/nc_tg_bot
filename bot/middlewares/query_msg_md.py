"""Query message middleware."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InaccessibleMessage, TelegramObject


class QueryMsgMD(BaseMiddleware):
    """Retrieves the message associated with a callback query and adds it to the data dictionary.

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
        """Calls the handler function with the injected Message instance."""
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)
        if isinstance(event.message, InaccessibleMessage):
            i18n = data.get("i18n")
            if i18n is None:
                msg = "i18n context is required but was not provided."
                raise TypeError(msg)
            text = i18n.get("msg-is-inaccessible")
            await event.answer(text)
            return None
        data.update({"query_msg": event.message})
        return await handler(event, data)
