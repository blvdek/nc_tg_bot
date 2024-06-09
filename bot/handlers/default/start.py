"""Start message handler."""

from aiogram.types import Message

from bot.core import settings
from bot.db import UnitOfWork
from bot.language import LocalizedTranslator


async def start(message: Message, translator: LocalizedTranslator, db: UnitOfWork) -> None:
    if await db.users.get_by_id(message.from_user.id):
        ...
        return
    await message.reply(text=translator.get("start", url=settings.nextcloud.url))
