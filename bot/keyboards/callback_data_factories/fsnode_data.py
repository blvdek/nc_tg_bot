"""Data for keyboards related to the fsnode menu."""

from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class FsNodeData(CallbackData, prefix="fsnode"):
    """The data passed when fsnode button is clicked.

    :param file_id: The ID of the file.
    :param page: The page number.
    """

    file_id: str
    page: int


class FsNodeMenuActions(IntEnum):
    """Actions that can be performed in the fsnode menu.

    :param PAG_NEXT: Move to the next page.
    :param PAG_BACK: Move to the previous page.
    :param DELETE: Delete a file.
    :param DELETE_CONFIRM: Confirm deletion of a file.
    :param DOWNLOAD: Download a file.
    :param NEW: Create a new file.
    :param UPLOAD:  Upload a file.
    :param MKDIR: Create a new dir.
    :param BACK: Go back to the previous dir.
    :param CANCEL: Cancel the current action.
    """

    PAG_NEXT = 0
    PAG_BACK = 1
    DELETE = 2
    DELETE_CONFIRM = 3
    DOWNLOAD = 4
    NEW = 5
    UPLOAD = 6
    MKDIR = 7
    BACK = 8
    CANCEL = 9


class FsNodeMenuData(CallbackData, prefix="fsnode_menu"):
    """The data passed when fsnode menu button is clicked.

    :param action: The action to be performed.
    :param file_id: The ID of the file.
    :param page: The page number of the file.
    """

    action: FsNodeMenuActions
    file_id: str
    page: int
