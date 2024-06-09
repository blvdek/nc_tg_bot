"""Authorization filter."""
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from bot.db import UnitOfWork
from bot.language import LocalizedTranslator


class AuthorizedFilter(BaseFilter):
    """Filter to check if the user is authorized"""

    async def __call__(self, event: TelegramObject, db: UnitOfWork, translator: LocalizedTranslator) -> bool:
        if await db.users.get_by_id(event.from_user.id):
            return True
        await event.reply(text=translator.get("not-authorized"))
        return False
