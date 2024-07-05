"""Main menu reply keyboard."""
from typing import Any

from aiogram.types import ReplyKeyboardMarkup
from aiogram_i18n import LazyProxy

from bot import keyboards


def menu_board(**kwargs: Any) -> ReplyKeyboardMarkup:
    """Create a reply keyboard with main menu buttons.

    :return: Reply keyboard markup with main menu buttons.
    """
    return keyboards.reply_board(
        LazyProxy("fsnode-menu-button"),
        LazyProxy("search-button"),
        LazyProxy("trashbin-button"),
        row_width=1,
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
        **kwargs,
    )
