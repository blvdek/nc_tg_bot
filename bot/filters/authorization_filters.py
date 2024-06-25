"""Authorization filter."""
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from bot.db import UnitOfWork


class AuthorizedFilter(BaseFilter):
    """Filter to check if the user is authorized with notice message."""

    async def __call__(self, event: TelegramObject, uow: UnitOfWork, i18n: I18nContext) -> bool:
        if await uow.users.get_by_id(event.from_user.id):
            return True
        await event.reply(text=i18n.get("not-authorized"))
        return False
