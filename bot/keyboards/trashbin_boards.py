"""Trash bin keyboards."""

from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards._fsnode_board_abstract import _FsNodeBaseBoard
from bot.keyboards.callback_data_factories import (
    TrashbinActions,
    TrashbinData,
    TrashbinFsNodeActions,
    TrashbinFsNodeData,
)


class TrashbinBoard(_FsNodeBaseBoard):
    """Keyboard for trashbin menu."""

    fsnode_callback_data = TrashbinFsNodeData
    actions_callback_data = TrashbinData
    actions = TrashbinActions

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        """Build buttons for trashbin actions.

        :return: InlineKeyboardBuilder object.
        """
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=LazyProxy("trashbin-cleanup-button"),
                callback_data=TrashbinData(
                    action=TrashbinActions.CLEANUP,
                    page=self.page,
                ).pack(),
            ),
        )
        return builder


def trashbin_cleanup_board(
    page: int = 0,
) -> InlineKeyboardMarkup:
    """Build keyboard for cleanup action.

    :param page: Page number.
    :return: InlineKeyboardMarkup object.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("confirm-button"),
                    callback_data=TrashbinData(
                        action=TrashbinActions.CLEANUP_CONFIRM,
                        page=page,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=LazyProxy("deny-button"),
                    callback_data=TrashbinData(
                        action=TrashbinActions.CANCEL,
                        page=page,
                    ).pack(),
                ),
            ],
        ],
    )


def trashbin_fsnode_board(file_id: str, page: int = 0) -> InlineKeyboardMarkup:
    """Build keyboard for fsnode in trashbin.

    :param file_id: The file id of the fsnode.
    :param page: Page number.
    :return: InlineKeyboardMarkup object.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("trashbin-delete-button"),
                    callback_data=TrashbinFsNodeData(
                        action=TrashbinFsNodeActions.DELETE,
                        page=page,
                        file_id=file_id,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=LazyProxy("trashbin-restore-button"),
                    callback_data=TrashbinFsNodeData(
                        action=TrashbinFsNodeActions.RESTORE,
                        page=page,
                        file_id=file_id,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=LazyProxy("back-button"),
                    callback_data=TrashbinData(
                        action=TrashbinActions.CANCEL,
                        page=page,
                    ).pack(),
                ),
            ],
        ],
    )
