"""Data for search keyboard."""
from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class SearchFsNodeData(CallbackData, prefix="search_fsnode"):
    """The data passed when fsnode button is clicked in search result.

    :param file_id: The ID of the file.
    :param page: The page number.
    :param from_user_id: Telegram user ID.
    """

    file_id: str
    page: int
    from_user_id: int


class SearchActions(IntEnum):
    """Actions that can be performed in the search keyboard.

    :param PAG_NEXT: Move to the next page.
    :param PAG_BACK: Move to the previous page.
    """

    PAG_NEXT = 0
    PAG_BACK = 1


class SearchData(CallbackData, prefix="search"):
    """The data passed when search button is clicked.

    :param action: The action to be performed.
    :param page: The page number of the file.
    :param from_user_id: Telegram user ID.
    :param query: The search query.
    """

    action: SearchActions
    page: int
    from_user_id: int
    query: str
