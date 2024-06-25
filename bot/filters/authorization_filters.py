"""Authorization filter."""
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram_i18n import I18nContext

from bot.db import UnitOfWork


class AuthorizedFilter(BaseFilter):
    """Filter to check if the user is authorized with notice message."""

    async def __call__(self, event: TelegramObject, uow: UnitOfWork, i18n: I18nContext) -> bool:
        if not isinstance(event, Message) or not isinstance(event, CallbackQuery):
            msg = "This filter is only usable with 'CallbackQuery' and 'Message' event types."
            raise TypeError(msg)
        if await uow.users.get_by_id(event.from_user.id):
            return True
        await event.reply(text=i18n.get("not-authorized"))
        return False
