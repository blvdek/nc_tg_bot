"""Data for trash bin keyboards."""
from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class TrashbinFsNodeActions(IntEnum):
    """Actions that can be performed on fsnode in trash bin.

    :param SELECT: Delete a file.
    :param DELETE: Delete a file.
    :param RESTORE: Delete a file.
    """

    SELECT = 0
    DELETE = 1
    RESTORE = 2


class TrashbinFsNodeData(CallbackData, prefix="trashbin_fsnode"):
    """The data passed when fsnode in trash bin button is clicked.

    :param action:
    :param file_id: The ID of the file.
    :param page: The page number.
    :param from_user_id: Telegram user ID.
    """

    action: TrashbinFsNodeActions = TrashbinFsNodeActions.SELECT
    file_id: str
    page: int
    from_user_id: int


class TrashbinActions(IntEnum):
    """Actions that can be performed on trash bin.

    :param SELECT: Delete a file.
    :param DELETE: Delete a file.
    :param RESTORE: Delete a file.
    """

    PAG_NEXT = 0
    PAG_BACK = 1
    CLEANUP = 2
    CLEANUP_CONFIRM = 3
    CANCEL = 4


class TrashbinData(CallbackData, prefix="trashbin"):
    """The data passed when trash bin button is clicked.

    :param action:
    :param file_id: The ID of the file.
    :param page: The page number.
    :param from_user_id: Telegram user ID.
    """

    action: TrashbinActions
    page: int
    from_user_id: int
