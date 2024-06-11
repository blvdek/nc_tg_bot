"""Start message handler."""

from aiogram.types import Message

from bot.core import settings
from bot.language import LocalizedTranslator


async def start(message: Message, translator: LocalizedTranslator) -> None:
    text = translator.get("start", url=settings.nextcloud.url)
    await message.reply(text=text)
