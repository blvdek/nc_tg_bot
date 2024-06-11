from typing import Any

from aiogram.types import ReplyKeyboardMarkup

from bot import keyboards
from bot.language import LocalizedTranslator


def menu_board(translator: LocalizedTranslator, **kwargs: Any) -> ReplyKeyboardMarkup:
    return keyboards.reply_board(translator.get("files-menu-button"), **kwargs)
