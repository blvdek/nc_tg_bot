"""Fsnode keyboards."""

from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup
from nc_py_api.files import FsNode

from bot.keyboards._fsnode_board_abstract import _FsNodeBaseBoard
from bot.keyboards.callback_data_factories import FsNodeData, FsNodeMenuActions, FsNodeMenuData


class FsNodeMenuBoard(_FsNodeBaseBoard):
    """Keyboard for fsnode menu.

    :param fsnode: File or directory to perform operations on.
    :param attached_fsnodes: List of files attached to the fsnode.
    :param kwargs: Additional parameters.
    """

    fsnode_callback_data = FsNodeData
    actions_callback_data = FsNodeMenuData
    actions = FsNodeMenuActions

    def __init__(
        self,
        fsnode: FsNode,
        attached_fsnodes: list[FsNode],
        **kwargs: Any,
    ) -> None:
        self.fsnode = fsnode
        super().__init__(attached_fsnodes, **kwargs, file_id=self.fsnode.file_id)

    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        """Build buttons for fsnode operations.

        :return: InlineKeyboardBuilder object.
        """
        builder = InlineKeyboardBuilder()
        if not self.fsnode.is_dir:
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-download-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.DOWNLOAD,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                    ).pack(),
                ),
            )
        if self.fsnode.is_dir and self.fsnode.is_creatable:
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-new-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.NEW,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                    ).pack(),
                ),
            )
        if self.fsnode.user_path != "" and self.fsnode.is_deletable:
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-delete-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.DELETE,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                    ).pack(),
                ),
            )
        if self.fsnode.user_path != "":
            builder.add(
                InlineKeyboardButton(
                    text=LazyProxy("back-button"),
                    callback_data=self.actions_callback_data(
                        action=self.actions.BACK,
                        file_id=self.fsnode.file_id,
                        page=self.page,
                    ).pack(),
                ),
            )
        builder.adjust(1)
        return builder


def fsnode_new_board(fsnode: FsNode, page: int = 0) -> InlineKeyboardMarkup:
    """Build keyboard with file or folder creation variants.

    :param fsnode: File or directory to delete.
    :param page: Page number.
    :return: InlineKeyboardMarkup object.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-upload-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.UPLOAD,
                        file_id=fsnode.file_id,
                        page=page,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=LazyProxy("fsnode-mkdir-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.MKDIR,
                        file_id=fsnode.file_id,
                        page=page,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=LazyProxy("cancel-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.CANCEL,
                        file_id=fsnode.file_id,
                        page=page,
                    ).pack(),
                ),
            ],
        ],
    )


def fsnode_delete_board(fsnode: FsNode, page: int = 0) -> InlineKeyboardMarkup:
    """Builds keyboard with confirm and deny buttons for deleting file or directory.

    :param fsnode: File or directory to delete.
    :param page: Page number.
    :return: InlineKeyboardMarkup object.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("confirm-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.DELETE_CONFIRM,
                        file_id=fsnode.file_id,
                        page=page,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=LazyProxy("deny-button"),
                    callback_data=FsNodeMenuData(
                        action=FsNodeMenuActions.CANCEL,
                        file_id=fsnode.file_id,
                        page=page,
                    ).pack(),
                ),
            ],
        ],
    )
