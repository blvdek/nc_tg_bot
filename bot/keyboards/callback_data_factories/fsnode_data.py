"""Data for keyboards related to the files."""
from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class FsNodeData(CallbackData, prefix="fsnode"):
    """The data passed when file button is clicked.

    :param file_id: The ID of the file.
    :param page: The page number of the file.
    :param author_id: Telegram ID of the user who triggered the message.
    """

    file_id: str
    page: int
    from_user_id: int


class FsNodeMenuActions(IntEnum):
    """Actions that can be performed in the files keyboard.

    :param SELECT: Select a file.
    :param PAG_NEXT: Move to the next page.
    :param PAG_BACK: Move to the previous page.
    :param DELETE: Delete a file.
    :param DELETE_CONFIRM: Confirm deletion of a file.
    :param DOWNLOAD: Download a file.
    :param UPLOAD:  Upload a file.
    :param CREATE_DIR: Create a new dir.
    :param UPDATE: Update a file.
    :param BACK: Go back to the previous dir.
    :param CANCEL: Cancel the current action.
    """

    PAG_NEXT = 0
    PAG_BACK = 1
    DELETE = 2
    DELETE_CONFIRM = 3
    DOWNLOAD = 4
    UPLOAD = 5
    MKDIR = 6
    BACK = 7
    CANCEL = 8


class FsNodeMenuData(CallbackData, prefix="fsnode_menu"):
    """The data passed when file button is clicked.

    :param action: The action to be performed.
    :param file_id: The ID of the file.
    :param page: The page number of the file.
    :param author_id: Telegram ID of the user who triggered the message.
    """

    action: FsNodeMenuActions
    file_id: str
    page: int
    from_user_id: int
