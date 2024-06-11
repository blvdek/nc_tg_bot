"""Data for keyboards related to the files."""
from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class FilesActions(IntEnum):
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

    SELECT = 0
    PAG_NEXT = 1
    PAG_BACK = 2
    DELETE = 3
    DELETE_CONFIRM = 4
    DOWNLOAD = 5
    UPLOAD = 6
    MKDIR = 7
    BACK = 8
    CANCEL = 9


class FilesData(CallbackData, prefix="files_menu"):
    """The data passed when file button is clicked.

    :param action: The action to be performed.
    :param page: The page number of the file.
    :param file_id: The ID of the file.
    :param author_id: Telegram ID of the user who triggered the message.
    """

    action: FilesActions
    page: int
    file_id: str
    author_id: int
