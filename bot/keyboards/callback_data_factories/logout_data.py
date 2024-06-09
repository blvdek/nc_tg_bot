"""Data for logout keyboard."""

import enum

from aiogram.filters.callback_data import CallbackData


class LogoutActions(enum.IntEnum):
    """Action can be performed in logout keyboard.

    :param confirm: Confirm logout.
    :param deny: Deny logout.
    """

    CONFIRM = 0
    DENY = 1


class LogoutData(CallbackData, prefix="logout"):
    """The data passed when button in logout keyboard is clicked.

    :param action: Confirm or deny logout.
    """

    action: LogoutActions
