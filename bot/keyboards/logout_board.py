"""An inline keyboard with logout buttons."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.callback_data_factories import LogoutActions, LogoutData
from bot.language import LocalizedTranslator


def logout_board(translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """Create an inline keyboard for logout.

    :param translator: An instance of LocalizedTranslator used to translate text into the user's preferred language.
    :return: InlineKeyboardMarkup object with two buttons for confirming or denying logout.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=translator.get("confirm-button"),
                    callback_data=LogoutData(action=LogoutActions.CONFIRM).pack(),
                ),
                InlineKeyboardButton(
                    text=translator.get("deny-button"),
                    callback_data=LogoutData(action=LogoutActions.DENY).pack(),
                ),
            ],
        ],
    )
