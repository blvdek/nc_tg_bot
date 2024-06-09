from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_board(
    *texts: str,
    is_persistent: bool | None = None,
    resize_keyboard: bool | None = None,
    one_time_keyboard: bool | None = None,
    selective: bool | None = None,
    input_field_placeholder: str | None = None,
    row_width: int = 2,
) -> ReplyKeyboardMarkup:
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=row_width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )
