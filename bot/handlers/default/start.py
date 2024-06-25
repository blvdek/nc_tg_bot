"""Start message handler."""

from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core import settings


async def start(message: Message, i18n: I18nContext) -> None:
    text = i18n.get("start", url=settings.nextcloud.url)
    await message.reply(text=text)
