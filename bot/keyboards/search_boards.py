"""Search menu keyboard."""

from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards._fsnode_board_abstract import _FsNodeBaseBoard
from bot.keyboards.callback_data_factories import SearchActions, SearchData, SearchFsNodeData


class SearchBoard(_FsNodeBaseBoard):
    """Keyboard for search menu.

    :param query: The search query.
    """

    fsnode_callback_data = SearchFsNodeData
    actions_callback_data = SearchData
    actions = SearchActions

    def __init__(self, query: str, **kwargs: Any) -> None:
        super().__init__(**kwargs, query=query)

    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        """Build buttons for search menu actions.

        :return: InlineKeyboardBuilder object.
        """
        return InlineKeyboardBuilder()
