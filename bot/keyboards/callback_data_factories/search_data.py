from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class SearchFsNodeData(CallbackData, prefix="search_fsnode"):
    file_id: str
    page: int
    from_user_id: int


class SearchActions(IntEnum):
    PAG_NEXT = 0
    PAG_BACK = 1


class SearchData(CallbackData, prefix="search"):
    action: SearchActions
    page: int
    from_user_id: int
    query: str
