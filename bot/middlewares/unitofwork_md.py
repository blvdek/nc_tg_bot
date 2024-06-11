from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db import UnitOfWork


class UnitOfWorkMD(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session_maker = data.get("_session_maker")
        if session_maker is None:
            msg = "'async_sessionmaker' object not found."
            raise RuntimeError(msg)
        async with UnitOfWork(session_maker) as uow:
            data["uow"] = uow
            return await handler(event, data)
