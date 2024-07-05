"""Function for creating a reply keyboard."""
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import KeyboardButton


def reply_board(
    *texts: LazyProxy,
    is_persistent: bool | None = None,
    resize_keyboard: bool | None = None,
    one_time_keyboard: bool | None = None,
    selective: bool | None = None,
    input_field_placeholder: str | None = None,
    row_width: int = 2,
) -> ReplyKeyboardMarkup:
    """Generates a reply keyboard markup with the given texts.

    :param *texts: The texts to be displayed on the keyboard.
    :param is_persistent: Whether the keyboard should be persistent, defaults to None.
    :param resize_keyboard: Whether the keyboard should be resized, defaults to None.
    :param one_time_keyboard: Whether the keyboard should be displayed only once, defaults to None.
    :param selective: Whether the keyboard should be selective, defaults to None.
    :param input_field_placeholder: The placeholder for the input field, defaults to None.
    :param row_width: The width of each row in the keyboard, defaults to 2.
    :return: Reply keyboard markup.
    """
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=row_width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )
