"""Authorization filter."""
from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject
from aiogram_i18n import I18nContext

from bot.db import UnitOfWork


class AuthorizedFilter(BaseFilter):
    """Filter to check if the user is authorized.

    This filter is used to verify whether the sender of a message is an authorized user.
    If the user is not authorized in Nextcloud, the bot sends a notification and blocks the execution of the command.
    """

    async def __call__(self, event: TelegramObject, uow: UnitOfWork, i18n: I18nContext) -> bool:
        """Checks if the user is authorized."""
        if not isinstance(event, Message):
            msg = "This filter is only usable with 'Message' event type."
            raise TypeError(msg)
        if event.from_user is None:
            msg = "Event object must have the 'from_user' attribute."
            raise AttributeError(msg)
        if await uow.users.get_by_id(event.from_user.id):
            return True
        await event.answer(text=i18n.get("not-authorized"))
        return False
