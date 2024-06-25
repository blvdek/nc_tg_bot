from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from nc_py_api import AsyncNextcloud

from bot.core import settings

if TYPE_CHECKING:
    from bot.db import UnitOfWork


class NextcloudMD(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        uow: UnitOfWork | None = data.get("uow")
        if uow is None:
            msg = "'UnitOfWork' object not found."
            raise RuntimeError(msg)
        if not isinstance(event, Message) or not isinstance(event, CallbackQuery):
            msg = "This middleware is only usable with 'CallbackQuery' and 'Message' event types."
            raise TypeError(msg)
        user = await uow.users.get_by_id(event.from_user.id)
        data["nc"] = AsyncNextcloud(
            nextcloud_url=settings.nextcloud.url,
            nc_auth_user=user.nc_login if user else None,
            nc_auth_pass=user.nc_app_password if user else None,
        )
        return await handler(event, data)
