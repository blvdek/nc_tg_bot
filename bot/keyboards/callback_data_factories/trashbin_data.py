from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class TrashbinFsNodeActions(IntEnum):
    SELECT = 0
    DELETE = 1
    RESTORE = 2


class TrashbinFsNodeData(CallbackData, prefix="trashbin_fsnode"):
    action: TrashbinFsNodeActions = TrashbinFsNodeActions.SELECT
    file_id: str
    page: int
    from_user_id: int


class TrashbinActions(IntEnum):
    PAG_NEXT = 0
    PAG_BACK = 1
    CLEANUP = 2
    CLEANUP_CONFIRM = 3
    CANCEL = 4


class TrashbinData(CallbackData, prefix="trashbin"):
    action: TrashbinActions
    page: int
    from_user_id: int
