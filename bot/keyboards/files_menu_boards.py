"""An inline keyboard with files menu, also inline deletion keyboard and cancel inline keyboard.

Deletion keyboard and cancel keyboard relate to files menu,
because they are called from the callbacks of the files menu.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from nc_py_api.files import FsNode

from bot.keyboards._files_board_abstract import _FilesBoardAbstract
from bot.keyboards.callback_data_factories import FilesMenuActions, FilesMenuData
from bot.language import LocalizedTranslator


class FilesMenuBoard(_FilesBoardAbstract):
    """Create an inline keyboard with files menu.

    :param translator: An instance of LocalizedTranslator used to translate text into the user's preferred language.
    :param file: A Nextcloud file object.
    :param files: _description_
    :param page: The current page number, defaults to 0.
    :param page_size: The number of files to display per page, defaults to DEFAULT_PAGE_SIZE.
    :return: InlineKeyboardMarkup object containing file buttoins, pagination and action buttons applied to files.
    """

    callback_data = FilesMenuData
    actions = FilesMenuActions

    def _build_file_actions_buttons(self) -> InlineKeyboardBuilder:
        act_builder = InlineKeyboardBuilder()
        if self.file.user_path != "" and self.file.is_deletable:
            act_builder.button(
                text=self.translator.get("file-delete-button"),
                callback_data=self.callback_data(
                    action=self.actions.DELETE,
                    page=self.page,
                    file_id=self.file.file_id,
                ).pack(),
            )
        if not self.file.is_dir:
            act_builder.button(
                text=self.translator.get("file-download-button"),
                callback_data=self.callback_data(
                    action=self.actions.DOWNLOAD,
                    page=self.page,
                    file_id=self.file.file_id,
                ).pack(),
            )
        if self.file.is_dir and self.file.is_creatable:
            act_builder.button(
                text=self.translator.get("file-upload-button"),
                callback_data=self.callback_data(
                    action=self.actions.UPLOAD,
                    page=self.page,
                    file_id=self.file.file_id,
                ).pack(),
            )
            act_builder.button(
                text=self.translator.get("file-mkdir-button"),
                callback_data=self.callback_data(
                    action=self.actions.MKDIR,
                    page=self.page,
                    file_id=self.file.file_id,
                ).pack(),
            )
        if self.file.user_path != "":
            act_builder.button(
                text=self.translator.get("file-back-button"),
                callback_data=self.callback_data(
                    action=self.actions.BACK,
                    page=self.page,
                    file_id=self.file.file_id,
                ).pack(),
            )
        act_builder.adjust(1)
        return act_builder


def files_menu_delete_board(translator: LocalizedTranslator, file: FsNode, page: int = 0) -> InlineKeyboardMarkup:
    """Create an inline keyboard for confirming or denying the deletion of a file or dir.

    :param translator: An instance of LocalizedTranslator used to translate text into the user's preferred language.
    :param file: A Nextcloud file object.
    :param page: The current page number, defaults to 0.
    :return: InlineKeyboardMarkup object containing confirming or denying the deletion of a file or dir buttons.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=translator.get("confirm-button"),
                    callback_data=FilesMenuData(
                        action=FilesMenuActions.DELETE_CONFIRM,
                        page=page,
                        file_id=file.file_id,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=translator.get("deny-button"),
                    callback_data=FilesMenuData(
                        action=FilesMenuActions.CANCEL,
                        page=page,
                        file_id=file.file_id,
                    ).pack(),
                ),
            ],
        ],
    )


def files_menu_cancel_board(translator: LocalizedTranslator, file: FsNode, page: int = 0) -> InlineKeyboardMarkup:
    """Create an inline keyboard that will allow user to cancel an operation or action.

    :param translator: An instance of LocalizedTranslator used to translate text into the user's preferred language.
    :param file: A Nextcloud file object.
    :param page: The current page number, defaults to 0.
    :return: InlineKeyboardMarkup object containing buttons that will allow user to cancel an operation or action.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=translator.get("file-cancel-button"),
                    callback_data=FilesMenuData(
                        action=FilesMenuActions.CANCEL,
                        page=page,
                        file_id=file.file_id,
                    ).pack(),
                ),
            ],
        ],
    )
