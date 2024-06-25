from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.callback_data_factories import SearchActions, SearchData, SearchFsNodeData
from bot.keyboards.fsnode_board_abstract import FsNodeBaseBoard


class SearchBoard(FsNodeBaseBoard):
    fsnode_callback_data = SearchFsNodeData
    actions_callback_data = SearchData
    actions = SearchActions

    def __init__(self, query: str, **kwargs: Any) -> None:
        super().__init__(**kwargs, query=query)

    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        return InlineKeyboardBuilder()
