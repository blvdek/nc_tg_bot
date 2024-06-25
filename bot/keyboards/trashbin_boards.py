from typing import Any

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.callback_data_factories import (
    TrashbinActions,
    TrashbinData,
    TrashbinFsNodeActions,
    TrashbinFsNodeData,
)
from bot.keyboards.fsnode_board_abstract import FsNodeBaseBoard


class TrashbinBoard(FsNodeBaseBoard):
    fsnode_callback_data = TrashbinFsNodeData
    actions_callback_data = TrashbinData
    actions = TrashbinActions

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        act_builder = InlineKeyboardBuilder()
        act_builder.add(
            InlineKeyboardButton(
                text=LazyProxy("trashbin-cleanup-button"),
                callback_data=TrashbinData(
                    action=TrashbinActions.CLEANUP,
                    page=self.page,
                    from_user_id=self.from_user_id,
                ).pack(),
            ),
        )
        return act_builder


def trashbin_cleanup_board(
    from_user_id: int,
    page: int = 0,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("confirm-button"),
                    callback_data=TrashbinData(
                        action=TrashbinActions.CLEANUP_CONFIRM,
                        page=page,
                        from_user_id=from_user_id,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=LazyProxy("deny-button"),
                    callback_data=TrashbinData(
                        action=TrashbinActions.CANCEL,
                        page=page,
                        from_user_id=from_user_id,
                    ).pack(),
                ),
            ],
        ],
    )


def trashbin_fsnode_board(
    from_user_id: int,
    file_id: str,
    page: int = 0,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("trashbin-delete-button"),
                    callback_data=TrashbinFsNodeData(
                        action=TrashbinFsNodeActions.DELETE,
                        page=page,
                        from_user_id=from_user_id,
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
                        from_user_id=from_user_id,
                        file_id=file_id,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=LazyProxy("cancel-button"),
                    callback_data=TrashbinData(
                        action=TrashbinActions.CANCEL,
                        page=page,
                        from_user_id=from_user_id,
                    ).pack(),
                ),
            ],
        ],
    )
