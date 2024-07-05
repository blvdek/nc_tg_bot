"""Default messages handlers."""
from aiogram import Bot
from aiogram.types import Message
from aiogram_i18n import I18nContext


async def start(message: Message, bot: Bot, i18n: I18nContext) -> None:
    """Handles the start command.

    :param message: Message object.
    :param bot: Bot object.
    :param i18n: Internationalization context.
    """
    bot_info = await bot.get_me()

    text = i18n.get("start", bot_name=bot_info.username)
    await message.reply(text=text)


async def help_msg(message: Message, i18n: I18nContext) -> None:
    """Handles the help message command.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    text = i18n.get("help")
    await message.reply(text=text)
